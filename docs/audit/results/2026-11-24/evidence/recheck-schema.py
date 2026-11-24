"""Independent read-only whole-build schema cross-check; no official validator claim."""
import collections
import hashlib
import json
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

BASE = Path('/Users/yavuz/prg/dr-cil')
EVIDENCE = BASE / 'docs/audit/results/2026-11-24/evidence'
BUILD = Path('/private/tmp/dr-cil-audit-2026-11-24/public')

class LD(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current = None
        self.scripts = []
        self.microdata = self.rdfa = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self.current = []
        self.microdata += int('itemscope' in a or 'itemtype' in a)
        self.rdfa += int('typeof' in a or 'vocab' in a)

    def handle_data(self, data):
        if self.current is not None:
            self.current.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.current is not None:
            self.scripts.append(''.join(self.current))
            self.current = None

def nodes(x):
    if isinstance(x, list):
        for v in x:
            yield from nodes(v)
    elif isinstance(x, dict):
        if '@graph' in x:
            yield from nodes(x['@graph'])
        else:
            yield x

out = {'timestamp_utc': datetime.now(timezone.utc).isoformat(),
       'build_root': str(BUILD), 'build_exists': BUILD.exists(),
       'official_validator_this_recheck': 'NOT_RUN',
       'html_count': 0, 'scripts': 0, 'parse_errors': [],
       'top_nodes': 0, 'top_types': collections.Counter(),
       'procedure_types': collections.Counter(), 'microdata_elements': 0,
       'rdfa_elements': 0, 'performer_nodes': 0,
       'nonsequential_breadcrumb_routes': [], 'conflicting_id_routes': [],
       'faq_duplicate_routes': [], 'source_sha256_match_initial': {}}
for p in sorted(BUILD.rglob('*.html')):
    out['html_count'] += 1
    page = LD()
    page.feed(p.read_text())
    out['microdata_elements'] += page.microdata
    out['rdfa_elements'] += page.rdfa
    all_nodes = []
    for s in page.scripts:
        out['scripts'] += 1
        try:
            all_nodes.extend(nodes(json.loads(s)))
        except Exception as exc:
            out['parse_errors'].append({'file': str(p.relative_to(BUILD)), 'error': str(exc)})
    ids = collections.defaultdict(set)
    nonsequential = False
    faq = 0
    for n in all_nodes:
        out['top_nodes'] += 1
        ts = n.get('@type', [])
        if isinstance(ts, str): ts = [ts]
        out['top_types'].update(ts)
        if '@id' in n:
            ids[n['@id']].add(json.dumps(n, sort_keys=True))
        if 'performer' in n: out['performer_nodes'] += 1
        if 'MedicalProcedure' in ts:
            out['procedure_types'][n.get('procedureType')] += 1
        if 'FAQPage' in ts: faq += 1
        if 'BreadcrumbList' in ts:
            actual = [x.get('position') for x in n.get('itemListElement', [])]
            nonsequential |= actual != list(range(1, len(actual)+1))
    rel = str(p.relative_to(BUILD))
    if nonsequential: out['nonsequential_breadcrumb_routes'].append(rel)
    if any(len(v) > 1 for v in ids.values()): out['conflicting_id_routes'].append(rel)
    if faq > 1: out['faq_duplicate_routes'].append(rel)
initial = json.loads((EVIDENCE / 'initial-worktree-state.json').read_text())
for f in ['layouts/partials/schema.html', 'layouts/partials/schema-procedure.html',
          'layouts/partials/schema-faq.html', 'layouts/partials/schema-scholarly.html',
          'scripts/check_schema.py', 'hugo.toml']:
    sha = hashlib.sha256((BASE/f).read_bytes()).hexdigest()
    out['source_sha256_match_initial'][f] = {'sha256': sha, 'matches': sha == initial['tracked_file_sha256'].get(f)}
out['notes'] = ['Static build evidence; no public HTTP, JSON-LD RDF expansion, clinical truth, Google indexing or official-validator result inferred.',
                'No missing @id classified as an error. Repeated ID checked within each page only.',
                'Nonsequential breadcrumb count is route count, not number of individual incorrect positions.']
(EVIDENCE / 'recheck-schema-output.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({k:(len(v) if k.endswith('_routes') else v) for k,v in out.items() if k not in ['source_sha256_match_initial','notes']}, ensure_ascii=False))
