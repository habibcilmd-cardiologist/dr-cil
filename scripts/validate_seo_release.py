#!/usr/bin/env python3
"""Independent emitted-output acceptance checks; no HTTP/index/ranking claims."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = ''; self.robots = ''; self.alias = False
        self.forms = []; self.fallback = False; self.ids = set()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = a.get('href','')
        if tag == 'meta' and a.get('name') == 'robots': self.robots = a.get('content','')
        if tag == 'meta' and a.get('http-equiv','').lower() == 'refresh': self.alias = True
        if tag == 'form': self.forms.append(a)
        if 'data-contact-fallback' in a: self.fallback = True

def read_pages(root):
    pages = {}
    for file in root.rglob('*.html'):
        page = Page(); page.feed(file.read_text())
        relative = file.relative_to(root).as_posix()
        path = '/' + (relative[:-10] if relative.endswith('index.html') else relative)
        pages[unquote(path)] = page
    return pages

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--before', type=Path, required=True)
    ap.add_argument('--after', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    before, after = read_pages(args.before), read_pages(args.after)
    errors = []; checks = []
    def check(name, passed, detail=None):
        checks.append({'name':name,'pass':bool(passed),'detail':detail})
        if not passed: errors.append(name)
    paths = ['/', '/', '/blog/diyabetik-ayak/', '/hizmetler/', '/hizmetler/',
             '/hizmetler/dizalti-damar-tikanikligi/', '/hizmetler/', '/blog/diyabetik-ayak/']
    for i, path in enumerate(paths, 1):
        page = after.get(path)
        check('keyword_target_'+str(i), page and not page.alias and 'noindex' not in page.robots
              and unquote(urlsplit(page.canonical).path)==path, path)
    check('existing_interventional_anchor', 'girisimsel-kardiyoloji' in after['/hizmetler/'].ids)
    before_canon = {p.canonical for p in before.values() if not p.alias and p.canonical}
    after_canon = {p.canonical for p in after.values() if not p.alias and p.canonical}
    check('all_prior_canonical_urls_preserved', not (before_canon-after_canon), sorted(before_canon-after_canon))
    rules = {}
    for line in (args.after/'_redirects').read_text().splitlines():
        parts=line.split()
        if len(parts)>=3 and not line.startswith('#'): rules[parts[0]]=parts[1:3]
    removed = sorted(set(before)-set(after))
    check('every_removed_html_route_has_explicit_301', all(p in rules and rules[p][1].startswith('301') for p in removed),removed)
    check('retired_home_rules_before_404', (args.after/'_redirects').read_text().index('/en/page/2/') < (args.after/'_redirects').read_text().index('/en/*'))
    check('legacy_home_rules_have_direct_targets', all(rules.get('/tr/page/'+str(i)+'/')==['/','301!'] for i in range(1,5)))
    success = ['/iletisim/tesekkurler/','/en/contact/thank-you/','/ar/contact/shukran/']
    for path in success:
        check('success_noindex_'+path, path in after and 'noindex' in after[path].robots)
    for path in ['/iletisim/','/en/contact/','/ar/contact/']:
        page=after[path]
        check('disabled_form_has_real_fallback_'+path, page.fallback and not any(f.get('name','').startswith('contact-') for f in page.forms))
    for prefix in ['', 'en/', 'ar/']:
        index=json.loads((args.after/prefix/'index.json').read_text())
        check('no_success_page_in_search_'+prefix, all(unquote(urlsplit(p['permalink']).path) not in success for p in index))
        check('search_language_fields_'+prefix, all(p.get('language') in ['tr','en','ar'] and p.get('languageName') for p in index))
    robots=(args.after/'robots.txt').read_text()
    for path in ['sitemap.xml','en/sitemap.xml','ar/sitemap.xml']:
        check('explicit_sitemap_'+path, (args.after/path).is_file() and 'https://docdrhabibcil.com/'+path in robots)
        text=(args.after/path).read_text()
        check('no_success_page_in_sitemap_'+path, all('/'+s.lstrip('/') not in text for s in success))
    count=sum('manual-taxonomy-content' in p.read_text() for p in args.after.rglob('*.html'))
    check('exact_taxonomy_links_rendered',count==53,count)
    report={'scope':'Static release acceptance; not real HTTP, browser, official schema, clinical or Google indexing validation',
            'before':str(args.before),'after':str(args.after),'html_before':len(before),'html_after':len(after),
            'checks':checks,'passed':sum(x['pass'] for x in checks),'error_count':len(errors),'errors':errors}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False))
    return int(bool(errors))

if __name__=='__main__':
    raise SystemExit(main())
