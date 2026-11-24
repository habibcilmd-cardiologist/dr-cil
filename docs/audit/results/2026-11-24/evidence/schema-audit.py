"""Read-only rendered JSON-LD inventory; not an official Schema.org validator.

Usage: python3 schema-audit.py BUILD_ROOT AUDIT_OUTPUT_DIRECTORY
All output is written beneath AUDIT_OUTPUT_DIRECTORY.
"""
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.scripts = []
        self.script = None
        self.hidden_depth = 0
        self.text = []
        self.canonicals = []
        self.refresh = None
        self.microdata = []
        self.rdfa = []
        self.title = []
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'script':
            self.script = [] if a.get('type', '').lower() == 'application/ld+json' else None
            self.hidden_depth += 1
        elif tag == 'style':
            self.hidden_depth += 1
        if tag == 'link' and a.get('rel', '').lower() == 'canonical':
            self.canonicals.append(a.get('href', ''))
        if tag == 'meta' and a.get('http-equiv', '').lower() == 'refresh':
            self.refresh = a.get('content', '')
        if 'itemscope' in a or 'itemtype' in a:
            self.microdata.append(a)
        if 'typeof' in a or 'vocab' in a:
            self.rdfa.append(a)
        if tag == 'title':
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == 'script':
            if self.script is not None:
                self.scripts.append(''.join(self.script))
            self.script = None
            self.hidden_depth = max(0, self.hidden_depth - 1)
        elif tag == 'style':
            self.hidden_depth = max(0, self.hidden_depth - 1)
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.script is not None:
            self.script.append(data)
        if not self.hidden_depth:
            self.text.append(data)
        if self.in_title:
            self.title.append(data)


def typed_nodes(obj):
    if isinstance(obj, dict):
        if '@type' in obj:
            yield obj
        for value in obj.values():
            yield from typed_nodes(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from typed_nodes(value)


def top_nodes(obj):
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]
    if isinstance(obj, dict):
        return obj.get('@graph', [obj])
    return []


def types(node):
    t = node.get('@type', [])
    return [t] if isinstance(t, str) else t


def output_exists(build, url):
    parsed = urlsplit(url)
    if parsed.netloc and parsed.netloc != 'docdrhabibcil.com':
        return None
    path = build / unquote(parsed.path).lstrip('/')
    return path.is_file() or (path / 'index.html').is_file()


build = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
evidence = out / 'evidence'
evidence.mkdir(parents=True, exist_ok=True)
pages = []
rows = []
issue_pages = defaultdict(set)
type_counts = Counter()
property_counts = Counter()
all_raw = []
for path in sorted(build.rglob('*.html')):
    html = path.read_text(encoding='utf-8')
    parsed = Page()
    parsed.feed(html)
    relative = path.relative_to(build).as_posix()
    route = '/' + relative
    if route.endswith('/index.html'):
        route = route[:-10]
    url = 'https://docdrhabibcil.com' + quote(route, safe='/%:@')
    lang = 'en' if route.startswith('/en/') else 'ar' if route.startswith('/ar/') else 'tr'
    page = {'file': relative, 'url': url, 'language': lang,
            'canonical': parsed.canonicals, 'refresh': parsed.refresh,
            'jsonld_script_count': len(parsed.scripts), 'parse_errors': [],
            'microdata': parsed.microdata, 'rdfa': parsed.rdfa,
            'top_nodes': [], 'issues': []}
    ids = defaultdict(list)
    for sn, raw in enumerate(parsed.scripts, 1):
        all_raw.append({'url': url, 'file': relative, 'script': sn,
                        'sha256': hashlib.sha256(raw.encode()).hexdigest(), 'raw_jsonld': raw})
        try:
            data = json.loads(raw)
        except Exception as error:
            page['parse_errors'].append({'script': sn, 'error': str(error)})
            issue_pages['SCHEMA_JSON_PARSE'].add(url)
            continue
        for node in typed_nodes(data):
            for t in types(node):
                type_counts[t] += 1
                for prop in node:
                    if not prop.startswith('@'):
                        property_counts[(t, prop)] += 1
        for nn, node in enumerate(top_nodes(data), 1):
            if not isinstance(node, dict):
                continue
            ts = types(node)
            issues = []
            if node.get('@id'):
                ids[node['@id']].append(node)
            if 'performer' in node and 'Event' not in ts:
                issues.append('SCHEMA_PERFORMER_DOMAIN')
            if 'MedicalProcedure' in ts:
                issues.append('SCHEMA_BLANKET_PROCEDURE_SEMANTICS_REVIEW')
                if node.get('procedureType') not in ['PercutaneousProcedure', 'NoninvasiveProcedure', 'https://schema.org/PercutaneousProcedure', 'https://schema.org/NoninvasiveProcedure']:
                    issues.append('SCHEMA_PROCEDURETYPE_NON_ENUM')
            if 'MedicalWebPage' in ts and node.get('reviewedBy'):
                issues.append('SCHEMA_REVIEW_EVIDENCE_MISSING')
            if 'ItemList' in ts and not node.get('itemListElement'):
                issues.append('SCHEMA_EMPTY_ITEMLIST')
            if 'MedicalBusiness' in ts:
                issues.append('SCHEMA_CLINIC_HOURS_CONFLICT')
            if ('Article' in ts or 'BlogPosting' in ts) and any(x in route for x in ['/tags/', '/categories/', '/page/']):
                issues.append('SCHEMA_LIST_AS_ARTICLE')
            if 'BreadcrumbList' in ts:
                positions = [x.get('position') for x in node.get('itemListElement', [])]
                if positions != list(range(1, len(positions)+1)):
                    issues.append('SCHEMA_BREADCRUMB_POSITIONS')
                for item in node.get('itemListElement', []):
                    target = item.get('item')
                    if isinstance(target, dict):
                        target = target.get('@id')
                    if isinstance(target, str) and output_exists(build, target) is False:
                        issues.append('SCHEMA_BREADCRUMB_MISSING_TARGET')
            if 'image' in node and isinstance(node['image'], str) and output_exists(build, node['image']) is False:
                issues.append('SCHEMA_IMAGE_MISSING_IN_BUILD')
            for issue in set(issues):
                issue_pages[issue].add(url)
            page['top_nodes'].append({'script': sn, 'node': nn, 'value': node, 'issues': sorted(set(issues))})
            rows.append({'url': url, 'language': lang, 'output_file': relative,
                         'script': sn, 'node': nn, 'types': '|'.join(ts),
                         'id': node.get('@id', ''), 'properties': '|'.join(sorted(k for k in node if not k.startswith('@'))),
                         'json_syntax': 'PASS', 'schema_vocabulary': ('TARGETED_DOMAIN_MISMATCH' if 'SCHEMA_PERFORMER_DOMAIN' in issues else 'TARGETED_ENUM_RANGE_MISMATCH' if 'SCHEMA_PROCEDURETYPE_NON_ENUM' in issues else 'NO_TARGETED_ERROR_FOUND;FULL_VALIDATOR_NOT_RUN'),
                         'google_feature': ('Breadcrumb' if 'BreadcrumbList' in ts else 'Article_candidate' if ('Article' in ts or 'BlogPosting' in ts or 'MedicalScholarlyArticle' in ts) else 'LocalBusiness_candidate' if ('MedicalBusiness' in ts or 'Physician' in ts) else 'FAQ_FEATURE_REMOVED_2026-05-07' if 'FAQPage' in ts else 'NO_DEDICATED_FEATURE'),
                         'official_validator': 'NOT_RUN', 'content_consistency': ('CONTRADICTION_WITH_CONTACT_HOURS' if 'MedicalBusiness' in ts else 'REVIEW_RECORD_NOT_VERIFIED' if node.get('reviewedBy') else 'SEMANTIC_REVIEW_REQUIRED' if 'MedicalProcedure' in ts else 'SEE_REPORT'),
                         'checks': '|'.join(sorted(set(issues)))})
    conflicts = []
    for identity, nodes in ids.items():
        if len(nodes) > 1:
            differing = set()
            for i, a in enumerate(nodes):
                for b in nodes[i+1:]:
                    differing.update(k for k in a.keys() & b.keys() if k not in ['@type', '@id', '@context'] and a[k] != b[k])
            if differing:
                conflicts.append({'id': identity, 'definitions': len(nodes), 'conflicting_properties': sorted(differing)})
                issue_pages['SCHEMA_CONFLICTING_ID'].add(url)
    page['conflicting_ids'] = conflicts
    page['issues'] = sorted({v for node in page['top_nodes'] for v in node['issues']} | ({'SCHEMA_CONFLICTING_ID'} if conflicts else set()))
    pages.append(page)

with (out / 'schema-inventory.csv').open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
summary = {'build_root': str(build), 'html_files_scanned': len(pages),
           'pages_with_jsonld': sum(bool(p['jsonld_script_count']) for p in pages),
           'jsonld_scripts': sum(p['jsonld_script_count'] for p in pages),
           'parse_errors': sum(len(p['parse_errors']) for p in pages),
           'top_node_rows': len(rows), 'typed_node_counts_including_nested': dict(type_counts),
           'type_property_counts': [{'type': t, 'property': p, 'count': n} for (t,p),n in sorted(property_counts.items())],
           'microdata_pages': sum(bool(p['microdata']) for p in pages),
           'rdfa_pages': sum(bool(p['rdfa']) for p in pages),
           'issue_page_counts': {k: len(v) for k,v in issue_pages.items()},
           'issue_pages': {k: sorted(v) for k,v in issue_pages.items()},
           'limitations': ['Static output only; not HTTP or browser execution', 'Not an official Schema.org validator', 'Automated issue flags include manual semantic-review candidates, not all proven faults']}
(evidence / 'schema-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
(evidence / 'schema-pages.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2))
(evidence / 'schema-jsonld-all.jsonl').write_text('\n'.join(json.dumps(p,ensure_ascii=False) for p in all_raw)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['issue_pages','type_property_counts']},ensure_ascii=False,indent=2))
