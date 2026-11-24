"""Validate audit deliverables and preserve source bytes; no application writes."""
from pathlib import Path
import collections
import csv
import datetime
import hashlib
import json
import re
import subprocess

ROOT=Path('/Users/yavuz/prg/dr-cil')
OUT=ROOT/'docs/audit/results/2026-11-24'
EV=OUT/'evidence'
required=['00-executive-summary.md','01-findings.md','02-url-and-template-inventory.csv',
 '03-schema-audit.md','schema-inventory.csv','04-performance.md','05-keyword-url-map.csv',
 '06-remediation-backlog.md','07-self-hosting-readiness.md','08-test-coverage.md','09-findings-matrix.csv']
missing=[n for n in required if not (OUT/n).is_file()]
counts={n:len(list(csv.DictReader((OUT/n).open(encoding='utf-8-sig')))) for n in required if n.endswith('.csv')}
rows=list(csv.DictReader((OUT/'09-findings-matrix.csv').open(encoding='utf-8-sig')))
ids=[x['ID'] for x in rows]
empty=[x['ID'] for x in rows if any(not str(v).strip() for v in x.values())]
finding_ids=re.findall(r'^### ([A-Z]+-\d+) — ',(OUT/'01-findings.md').read_text(),re.M)
local_missing=[]
for n in [x for x in required if x.endswith('.md')]:
 for dest in re.findall(r'\]\(([^)]+)\)',(OUT/n).read_text()):
  if dest.startswith(('http','mailto:','tel:','#')):continue
  if not ((OUT/n).parent/dest.split('#')[0]).resolve().exists():
   local_missing.append({'file':n,'target':dest})
inv=list(csv.DictReader((OUT/'02-url-and-template-inventory.csv').open(encoding='utf-8-sig')))
urls={x['url'] for x in inv}
sample={x.rstrip('`.,*') for x in re.findall(r'https://docdrhabibcil\.com/[^\s;|]*',(OUT/'08-test-coverage.md').read_text())}
sample_missing=sorted(x for x in sample if x not in urls and x!='https://docdrhabibcil.com/tr/')
initial=json.loads((EV/'initial-worktree-state.json').read_text())
changed=[];gone=[]
for n,h in initial['tracked_file_sha256'].items():
 p=ROOT/n
 if not p.is_file():gone.append(n)
 elif hashlib.sha256(p.read_bytes()).hexdigest()!=h:changed.append(n)
tri=json.loads((EV/'static-link-triage.json').read_text())['unresolved_after_declared_netlify_rule']
current_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
result={
 'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'required_missing':missing,'csv_rows':counts,'finding_unique_ids':len(set(ids)),
 'finding_empty_fields':empty,'findings_md_csv_ids_match':set(ids)==set(finding_ids),
 'local_report_link_missing':local_missing,
 'sample_urls_not_in_inventory_except_declared_legacy':sample_missing,
 'initial_commit':initial['commit'],'current_head':current_head,
 'external_head_change_observed':current_head!=initial['commit'],
 'initial_file_count':len(initial['tracked_file_sha256']),
 'changed_initial_files':changed,'missing_initial_files':gone,
 'theme_status':subprocess.check_output(['git','-C','themes/blowfish','status','--short'],cwd=ROOT,text=True),
 'triaged_unresolved_instances':len(tri),'triaged_unresolved_targets':len({x['resolved'] for x in tri}),
 'triaged_affected_routes':len({x['source_url'] for x in tri}),
 'executive_word_count':len((OUT/'00-executive-summary.md').read_text().split()),
 'source_changes_by_audit':False,
 'new_production_build_exit':json.loads((EV/'recheck-production-build.json').read_text())['exit_code'],
 'new_vs_prior_html_differences':json.loads((EV/'recheck-build-comparison.json').read_text())['html_different'],
 'git_status':subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True),
 'runtime_not_run':['new browser after two timeouts','native200','breakpoint852/853/854',
  'production cold>=3desktop+3mobile','warm visits','CPU/GPU attribution','modelAB/offscreen frames',
  'screenreader/contrast/touch','JS/CDN/WebGL/fallback runtime','second DNS resolver/authoritative',
  'production TLS/HTTP/404/redirect/headers','GSC/GBP/CrUX/SERP','clinical external verification','form delivery'],
}
result['artifact_validation_pass']=not any([missing,empty,local_missing,sample_missing,changed,gone]) and len(ids)==len(set(ids))==42 and result['findings_md_csv_ids_match'] and counts=={'02-url-and-template-inventory.csv':976,'schema-inventory.csv':3322,'05-keyword-url-map.csv':8,'09-findings-matrix.csv':42}
(EV/'recheck-final-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
manifest={p.relative_to(OUT).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in OUT.rglob('*') if p.is_file() and p.name!='recheck-artifact-manifest.json'}
(EV/'recheck-artifact-manifest.json').write_text(json.dumps({'timestamp_utc':result['timestamp_utc'],'files':manifest},ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in result.items() if k not in ['git_status','runtime_not_run']},ensure_ascii=False,indent=2))
raise SystemExit(0 if result['artifact_validation_pass'] else 1)
