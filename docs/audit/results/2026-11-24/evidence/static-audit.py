#!/usr/bin/env python3
"""Read-only crawl of an isolated Hugo output; no HTTP results are inferred."""
import argparse, collections, csv, hashlib, json, re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import xml.etree.ElementTree as ET

BASE='https://docdrhabibcil.com/'
OWN={'docdrhabibcil.com','www.docdrhabibcil.com'}
NS={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}

def text(value): return re.sub(r'\s+',' ',value).strip()
def language(url):
    p=urlsplit(url).path
    return 'en' if p.startswith('/en/') else 'ar' if p.startswith('/ar/') else 'tr'
def norm(url):
    u=urlsplit(url); path=unquote(u.path)
    return (u.scheme or 'https', (u.hostname or 'docdrhabibcil.com').lower(),path)

class Page(HTMLParser):
    def __init__(self,path,root):
        super().__init__(convert_charrefs=True)
        self.path=path; self.relative=path.relative_to(root).as_posix()
        self.url=BASE+(self.relative[:-10] if self.relative.endswith('index.html') else self.relative)
        self.title=[]; self.h1=[]; self.headings=[]; self.ids=set(); self.links=[]; self.assets=[]
        self.metas=[]; self.canon=[]; self.alternates=[]; self.lang=''; self.refresh=''; self._capture=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html': self.lang=a.get('lang','')
        if a.get('id'): self.ids.add(a['id'])
        if tag=='a' and a.get('name'): self.ids.add(a['name'])
        if tag=='title': self._capture.append(['title',[]])
        if re.fullmatch('h[1-6]',tag): self._capture.append([tag,[]])
        if tag=='meta':
            self.metas.append(a)
            if a.get('http-equiv','').lower()=='refresh': self.refresh=a.get('content','')
        if tag=='a' and a.get('href'): self.links.append(a['href'])
        if tag=='link':
            rel=a.get('rel','').lower().split()
            if 'canonical' in rel: self.canon.append(a.get('href',''))
            if 'alternate' in rel and a.get('hreflang'): self.alternates.append((a['hreflang'],a.get('href','')))
            if any(r in rel for r in ['stylesheet','icon','manifest','preload','modulepreload']) and a.get('href'): self.assets.append((tag,a['href']))
        if tag in ['img','script','video','source','audio','iframe'] and a.get('src'): self.assets.append((tag,a['src']))
        if tag=='video' and a.get('poster'): self.assets.append(('poster',a['poster']))
        if tag in ['source','img'] and a.get('srcset'):
            for src in a['srcset'].split(','):
                if src.strip(): self.assets.append(('srcset',src.strip().split()[0]))
    def handle_data(self,data):
        for capture in self._capture: capture[1].append(data)
    def handle_endtag(self,tag):
        for i in range(len(self._capture)-1,-1,-1):
            if self._capture[i][0]==tag:
                kind,value=self._capture.pop(i);value=text(''.join(value))
                if kind=='title': self.title.append(value)
                else:
                    self.headings.append((kind,value))
                    if kind=='h1': self.h1.append(value)
                break
    def finish(self):
        self.alias=''
        if self.refresh:
            m=re.search(r'url\s*=\s*(.+)',self.refresh,re.I)
            if m: self.alias=m.group(1).strip(' \"\'')
        self.robots=[a.get('content','') for a in self.metas if a.get('name','').lower() in ['robots','googlebot']]
        self.noindex=any('noindex' in x.lower() for x in self.robots)
        self.description=[a.get('content','') for a in self.metas if a.get('name','').lower()=='description']
        self.kind='alias' if self.alias else '404' if self.relative.endswith('404.html') else 'pagination' if re.search(r'/page/\d+/',self.url) else 'home' if urlsplit(self.url).path in ['/','/en/','/ar/'] else 'taxonomy' if re.search(r'/(tags|categories)/',self.url) else 'content_or_section'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('output');args=ap.parse_args()
    root=Path(args.root); out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    pages=[]
    for path in sorted(root.rglob('*.html')):
        p=Page(path,root);p.feed(path.read_text(encoding='utf8'));p.finish();pages.append(p)
    by_url={norm(p.url):p for p in pages};by_path={p.path:p for p in pages};by_canonical={norm(p.canon[0]):p for p in pages if p.canon and not p.alias and p.kind!='404'}
    def resolve(url,source):
        try: u=urlsplit(urljoin(source,url))
        except ValueError:return None,None,'invalid_url'
        if u.scheme not in ['http','https'] or u.hostname not in OWN:return None,u,'external'
        path=unquote(u.path).lstrip('/')
        target=root/path
        if u.path.endswith('/') or target.is_dir():target=target/'index.html'
        if not target.is_file():return target,u,'missing'
        return target,u,'exists'
    broken_links=[];broken_assets=[];broken_fragments=[];alias_links=[];canon_issues=[];hreflang_issues=[];rows=[]
    inbound=collections.Counter(); duplicate_hreflang=[];heading_issues=[]
    for p in pages:
        missing_links=[];missing_assets=[]
        if not p.alias and p.kind!='404':
            for href in p.links:
                target,u,status=resolve(href,p.url)
                if status=='missing':
                    item={'source_url':p.url,'href':href,'resolved':u.geturl(),'expected_file':str(target.relative_to(root))}
                    broken_links.append(item);missing_links.append(href)
                elif status=='exists' and target.suffix=='.html':
                    key=norm(u.geturl()); dest=by_url.get(key)
                    if not dest and target:dest=by_path.get(target)
                    if dest:
                        if dest.url!=p.url:inbound[dest.url]+=1
                        if dest.alias:alias_links.append({'source_url':p.url,'href':href,'alias_target':dest.alias})
                        elif u.fragment and not u.fragment.startswith(':~:') and unquote(u.fragment) not in dest.ids:
                            broken_fragments.append({'source_url':p.url,'href':href,'resolved':u.geturl(),'fragment':unquote(u.fragment)})
            for tag,src in p.assets:
                target,u,status=resolve(src,p.url)
                if status=='missing':
                    broken_assets.append({'source_url':p.url,'tag':tag,'src':src,'resolved':u.geturl(),'expected_file':str(target.relative_to(root))});missing_assets.append(src)
            if len(p.canon)!=1:canon_issues.append({'url':p.url,'issue':'canonical_count','values':p.canon})
            for c in p.canon:
                target,u,status=resolve(c,p.url)
                if status!='exists':canon_issues.append({'url':p.url,'issue':'canonical_target_'+status,'value':c})
                elif norm(c)!=norm(p.url):canon_issues.append({'url':p.url,'issue':'canonical_not_self','value':c})
            groups=collections.defaultdict(list)
            for hl,href in p.alternates:groups[hl].append(href)
            for hl,hrefs in groups.items():
                if len(hrefs)>1:duplicate_hreflang.append({'url':p.url,'hreflang':hl,'values':hrefs,'conflicting':len(set(hrefs))>1})
            if p.alternates and not any(norm(href)==norm(p.url) for hl,href in p.alternates if hl!='x-default'):
                hreflang_issues.append({'url':p.url,'issue':'missing_self','alternates':p.alternates})
            for hl,href in p.alternates:
                target,u,status=resolve(href,p.url)
                if status!='exists':hreflang_issues.append({'url':p.url,'issue':'target_'+status,'hreflang':hl,'target':href});continue
                dest=by_url.get(norm(href))
                if dest and hl!='x-default':
                    if dest.alias:hreflang_issues.append({'url':p.url,'issue':'target_alias','hreflang':hl,'target':href})
                    elif not any(norm(back)==norm(p.url) for key,back in dest.alternates if key!='x-default'):
                        hreflang_issues.append({'url':p.url,'issue':'missing_reciprocal','hreflang':hl,'target':href})
                    if language(href)!=hl.split('-')[0].lower():hreflang_issues.append({'url':p.url,'issue':'language_mismatch','hreflang':hl,'target':href})
            if len(p.h1)!=1:heading_issues.append({'url':p.url,'h1_count':len(p.h1),'h1':p.h1})
        rows.append({'url':p.url,'file':p.relative,'language':language(p.url),'html_lang':p.lang,'classification':p.kind,'http_status':'not_measured','alias_target':p.alias,'canonical':' | '.join(p.canon),'canonical_self':bool(p.canon and norm(p.canon[0])==norm(p.url)),'robots':' | '.join(p.robots),'indexability_static':'alias' if p.alias else '404' if p.kind=='404' else 'noindex' if p.noindex else 'potentially_indexable_http_unverified','title':' | '.join(p.title),'h1_count':len(p.h1),'h1':' | '.join(p.h1),'description':' | '.join(p.description),'hreflang_count':len(p.alternates),'missing_links_count':len(missing_links),'missing_assets_count':len(missing_assets)})
    source_csv=out/'static-source-content.csv'
    source_rows=list(csv.DictReader(source_csv.open())) if source_csv.exists() else []
    source_by_url={norm(r['permalink']):r for r in source_rows}
    for row in rows:
        row['inbound_static_link_count']=inbound[row['url']]
        item=source_by_url.get(norm(row['url'])) or (source_by_url.get(norm(row['canonical'])) if row['canonical'] else None)
        row['source_content']=item['path'] if item else ''
        row['hugo_source_kind']=item['kind'] if item else ''
        row['source_section']=item['section'] if item else ''
        cl=row['classification']
        layout=''
        if item:
            content_path=Path(item['path'])
            if content_path.is_file():
                match=re.search(r'^layout:\s*[\"\']?([^\"\'\n]+)',content_path.read_text(),re.M)
                if match:layout=match.group(1).strip()
        row['template_family']='alias (Hugo generated)' if cl=='alias' else 'layouts/404.html' if cl=='404' else 'themes/blowfish/layouts/index.html → home/profile+hero' if cl=='home' or cl=='pagination' and norm(row['canonical'])[2] in ['/','/en/','/ar/'] else 'themes/blowfish/layouts/_default/'+layout+'.html (front matter layout)' if layout else 'layouts/_default/single.html' if item and item['kind']=='page' else 'themes/blowfish/layouts/_default/terms.html' if re.search(r'/(tags|categories)/$',urlsplit(row['url']).path) else 'themes/blowfish/layouts/_default/list.html'
    with (out.parent/'02-url-and-template-inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    def dump(name,data):(out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
    dump('static-broken-links.json',broken_links);dump('static-broken-assets.json',broken_assets);dump('static-broken-fragments.json',broken_fragments)
    triaged=[]
    for item in broken_links:
        item=dict(item);path=urlsplit(item['resolved']).path
        if path.startswith('/tr/'):
            new=path[3:];target,u,status=resolve(new,BASE)
            item['declared_netlify_redirect_target']=BASE.rstrip('/')+new
            item['target_after_declared_redirect_exists']=status=='exists'
        else:item['target_after_declared_redirect_exists']=False
        triaged.append(item)
    recoverable=[r for r in triaged if r['target_after_declared_redirect_exists']]
    unresolved=[r for r in triaged if not r['target_after_declared_redirect_exists']]
    dump('static-link-triage.json',{'static_missing_instances':len(triaged),'netlify_tr_rule_recoverable_instances':len(recoverable),'unresolved_even_after_declared_tr_rule_instances':len(unresolved),'recoverable_under_declared_netlify_rule':recoverable,'unresolved_after_declared_netlify_rule':unresolved,'limitations':'Declared /tr/* redirects evaluated as configuration only; actual HTTP redirect was not measured.'})
    dump('static-alias-links.json',alias_links);dump('static-canonical-issues.json',canon_issues);dump('static-hreflang-issues.json',hreflang_issues);dump('static-hreflang-duplicates.json',duplicate_hreflang);dump('static-heading-issues.json',heading_issues)
    actual=[p for p in pages if not p.alias and p.kind!='404']
    titles=collections.defaultdict(list);descs=collections.defaultdict(list)
    for p in actual:
        if p.title:titles[' | '.join(p.title)].append(p.url)
        if p.description:descs[' | '.join(p.description)].append(p.url)
    dump('static-duplicate-titles.json',{k:v for k,v in titles.items() if len(v)>1});dump('static-duplicate-descriptions.json',{k:v for k,v in descs.items() if len(v)>1})
    sitemaps=[]; sitemap_urls=set()
    for path in sorted(root.rglob('*sitemap*.xml')):
        try:
            tree=ET.parse(path).getroot();entries=[]
            for e in tree.findall('s:url',NS):
                loc=e.findtext('s:loc','',NS);sitemap_urls.add(norm(loc));target,u,status=resolve(loc,BASE)
                entries.append({'loc':loc,'lastmod':e.findtext('s:lastmod','',NS),'target_status_static':status})
            sitemaps.append({'file':path.relative_to(root).as_posix(),'root_type':tree.tag.split('}')[-1],'entries':len(entries),'unique_locs':len(set(e['loc'] for e in entries)),'missing_targets':[e for e in entries if e['target_status_static']!='exists'],'child_sitemaps':[e.text for e in tree.findall('s:sitemap/s:loc',NS)],'urls':entries})
        except Exception as e:sitemaps.append({'file':str(path),'error':str(e)})
    dump('static-sitemaps.json',sitemaps)
    missing_sitemap=[p.url for p in actual if not p.noindex and p.kind!='pagination' and norm(p.url) not in sitemap_urls]
    dump('static-not-in-any-sitemap.json',missing_sitemap)
    search=[]
    for prefix in ['','en/','ar/']:
        path=root/prefix/'index.json'
        if path.exists():
            data=json.loads(path.read_text());counts=collections.Counter(language(e.get('permalink','')) for e in data)
            search.append({'file':prefix+'index.json','sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'entries':len(data),'permalink_languages':dict(counts),'examples_foreign':[{'title':e.get('title'),'permalink':e.get('permalink')} for e in data if language(e.get('permalink',''))!=language(BASE+prefix)][:12]})
    dump('static-search-indexes.json',search)
    dump('static-orphan-candidates.json',[{'url':p.url,'kind':p.kind} for p in actual if not inbound[p.url]])
    summary={'root':str(root),'html_total':len(pages),'by_language':dict(collections.Counter(language(p.url) for p in pages)),'by_classification':dict(collections.Counter(p.kind for p in pages)),'actual_non_alias_non404':len(actual),'actual_language_counts':dict(collections.Counter(language(p.url) for p in actual)),'noindex_actual':sum(p.noindex for p in actual),'unique_canonicals':len({norm(p.canon[0]) for p in actual if p.canon}),'missing_descriptions':sum(not p.description for p in actual),'missing_titles':sum(not p.title for p in actual),'broken_link_instances':len(broken_links),'broken_link_unique_targets':len({x['resolved'] for x in broken_links}),'broken_link_affected_pages':len({x['source_url'] for x in broken_links}),'broken_asset_instances':len(broken_assets),'broken_asset_unique_targets':len({x['resolved'] for x in broken_assets}),'broken_fragment_instances':len(broken_fragments),'alias_link_instances':len(alias_links),'canonical_issues':len(canon_issues),'hreflang_issues':len(hreflang_issues),'duplicate_hreflang_groups':len(duplicate_hreflang),'conflicting_hreflang_groups':sum(x['conflicting'] for x in duplicate_hreflang),'heading_issues':len(heading_issues),'sitemaps':[{k:v for k,v in x.items() if k not in ['urls']} for x in sitemaps],'not_in_any_sitemap_nonpagination':len(missing_sitemap),'search_indexes':search,'orphan_candidates':sum(not inbound[p.url] for p in actual),'limitations':['No HTTP requests/status codes inferred; local file existence only.','DOM text and heading counts include all emitted elements; browser visibility not inferred.','Source template/category classification inferred from output URL except aliases/404/home.','Anchor targets are checked against emitted id/name only; JS-created destinations may create false positives.','Duplicate titles/descriptions can be legitimate on pagination; review before severity assignment.']}
    dump('static-summary.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k not in ['sitemaps','search_indexes','limitations']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
