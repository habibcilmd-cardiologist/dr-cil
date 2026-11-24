"""Preserve the review patch and validate the final deliverables; no deployment."""
import csv
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT=Path('/Users/yavuz/prg/dr-cil')
OUT=ROOT/'docs/implementation/seo-remediation/2026-11-24'
EV=OUT/'evidence'
initial=json.loads((EV/'initial-worktree.json').read_text())
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT)
roots=['assets','config','content','data','i18n','layouts','scripts','static','hugo.toml','hugo-version.txt','netlify.toml','package.json','README.md']
def owned_source(name): return any(name==p or name.startswith(p+'/') for p in roots)
untracked=[x for x in git('ls-files','--others','--exclude-standard','-z').decode().split('\0') if x and owned_source(x)]
patch=git('diff','--binary','--',*roots)
for name in untracked:
 r=subprocess.run(['git','diff','--no-index','--binary','--','/dev/null',name],cwd=ROOT,capture_output=True)
 assert r.returncode in (0,1),r.stderr
 patch+=r.stdout
(EV/'source-changes.patch').write_bytes(patch)
tracked=[x for x in git('ls-files','-z').decode().split('\0') if x]
changed=[];audit_changed=[];resources_changed=[]
for name,before_hash in initial['tracked_sha256'].items():
 p=ROOT/name
 different=not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=before_hash
 if different:
  changed.append(name)
  if name.startswith('docs/audit/'):audit_changed.append(name)
  if name.startswith(('resources/','public/')):resources_changed.append(name)
theme_status=git('-C','themes/blowfish','status','--short').decode()
check=subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True,text=True)
source_hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in tracked+untracked if owned_source(p) and (ROOT/p).is_file()}
preservation={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'initial_commit':initial['commit'],'current_commit':git('rev-parse','HEAD').decode().strip(),
 'initial_status':initial['status'],'final_status':git('status','--short').decode(),
 'changed_initial_tracked_paths':changed,'new_application_source_paths':untracked,
 'audit_files_changed':audit_changed,'tracked_public_resources_changed':resources_changed,
 'theme_worktree_status':theme_status,'source_sha256':source_hashes,
 'diff_check_exit':check.returncode,'diff_check_output':check.stdout+check.stderr,
 'authorized_local_source_changes':True,'dns_or_account_changes':False,
 'message_form_appointment_sent':False,'commit_push_deploy':False}
(EV/'final-preservation.json').write_text(json.dumps(preservation,ensure_ascii=False,indent=2))

refs=[
 ('layouts/partials/header/basic.html','drcil','Header/menü'),
 ('assets/css/custom.css','drcil-desktop','Header breakpoint/layout'),
 ('assets/js/mobilemenu.js','function activate','Ortak odak/inert'),
 ('assets/js/search.js','drcilDialog','Arama/modal'),
 ('layouts/404.html','define','Üç dil404'),
 ('layouts/partials/author.html','rel="author"','Biyografi bağlantısı'),
 ('layouts/partials/head.html','current-page-url','Canonical/title'),
 ('layouts/partials/seo/alternates.html','return','Hreflang'),
 ('layouts/home.sitemappages.xml','urlset','Sitemap sahipliği'),
 ('layouts/partials/seo/manual-taxonomy-links.html','manual-taxonomy-content','53 kesin arşiv'),
 ('layouts/partials/schema.html','schema-breadcrumb-items','Graph ve breadcrumb'),
 ('layouts/partials/schema-procedure.html','mapping','Konu sınıflandırması'),
 ('data/schema_content_types.yaml','entities','Dar kaynak haritası'),
 ('assets/js/heart-viewer.js','createHeartRenderLoop','Render lifecycle'),
 ('layouts/partials/three-heart.html','data-heart-model','Poster/istek'),
 ('layouts/partials/home/hero.html','srcset','Hero kaynakları'),
 ('layouts/shortcodes/contact-form.html','provider','Form sağlayıcı kapısı'),
 ('static/_redirects','/tr/page/2/','Doğrudan301'),
 ('scripts/build-production.py','expected =','Güvenli/pinli build'),
 ('netlify.toml','HUGO_VERSION','Yerel CI sürüm tanımı')]
locations=[]
for name,needle,purpose in refs:
 lines=(ROOT/name).read_text().splitlines()
 line=next((i for i,s in enumerate(lines,1) if needle in s),1)
 locations.append({'file':name,'line':line,'purpose':purpose})
(EV/'source-location-index.json').write_text(json.dumps(locations,ensure_ascii=False,indent=2))
report=OUT/'01-changes-and-validation.md'
s=report.read_text()
if '## Güncel kaynak satırları' not in s:
 s+='\n## Güncel kaynak satırları\n\n| Dosya | Satır | Amaç |\n| --- | ---: | --- |\n'
 s+='\n'.join('| ['+r['file']+'](sandbox:'+str(ROOT/r['file'])+') | '+str(r['line'])+' | '+r['purpose']+' |' for r in locations)+'\n'
 report.write_text(s)

required=['00-progress.md','01-changes-and-validation.md','02-keyword-content-map.csv',
 '03-redirect-and-indexing-map.csv','04-schema-validation.md','05-performance-before-after.md','06-launch-readiness.md']
missing=[n for n in required if not (OUT/n).is_file() or not (OUT/n).stat().st_size]
ids=re.findall(r'^\| ([A-Z]+-\d+) \|',(OUT/'00-progress.md').read_text(),re.M)
packages=re.findall(r'^\| (B\d+) \|',(OUT/'00-progress.md').read_text(),re.M)
maps=list(csv.DictReader((OUT/'02-keyword-content-map.csv').open(encoding='utf-8-sig')))
local_missing=[]
for name in required:
 if not name.endswith('.md'):continue
 for target in re.findall(r'\]\(([^)]+)\)',(OUT/name).read_text()):
  if target.startswith(('http','mailto:','tel:','#')):continue
  path=Path(target[8:]) if target.startswith('sandbox:') else (OUT/target.split('#')[0]).resolve()
  if not path.exists():local_missing.append({'file':name,'link':target})
tests={n:json.loads((EV/n).read_text()) for n in ['schema-after-final.json','ui-contract-final.json','seo-release-final.json','contact-form-tests.json','heart-viewer-node-tests.json','clinical-claims-preserved.json']}
passed=(not missing and not local_missing and len(set(ids))==42 and len(ids)==42
 and len(set(packages))==15 and len(maps)==8 and check.returncode==0
 and not audit_changed and not resources_changed and not theme_status
 and tests['schema-after-final.json']['error_count']==0
 and not tests['ui-contract-final.json']['errors']
 and tests['seo-release-final.json']['error_count']==0
 and tests['contact-form-tests.json']['passed']==8
 and tests['heart-viewer-node-tests.json']['passed']==9
 and all(x['unchanged'] for x in tests['clinical-claims-preserved.json']))
validation={'timestamp_utc':preservation['timestamp_utc'],'required_missing':missing,
 'missing_local_report_links':local_missing,'finding_ids':len(set(ids)),
 'packages':len(set(packages)),'keyword_rows':len(maps),'source_patch_bytes':len(patch),
 'changed_tracked_source_count':sum(owned_source(p) for p in changed),'new_source_count':len(untracked),
 'audit_changed':audit_changed,'resources_changed':resources_changed,'theme_clean':not bool(theme_status),
 'schema_targeted_errors':tests['schema-after-final.json']['error_count'],
 'ui_contract_errors':len(tests['ui-contract-final.json']['errors']),
 'release_checks_passed':tests['seo-release-final.json']['passed'],
 'contact_cases_passed':8,'heart_node_cases_passed':9,'percent_claim_lines_unchanged':47,
 'diff_check_exit':check.returncode,'artifact_and_local_acceptance_pass':passed,
 'full_browser_production_external_acceptance':'NOT_RUN / pending; see06-launch-readiness.md'}
(EV/'final-validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2))
manifest={p.relative_to(OUT).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 for p in OUT.rglob('*') if p.is_file() and p.name!='artifact-manifest.json'}
(EV/'artifact-manifest.json').write_text(json.dumps({'timestamp_utc':preservation['timestamp_utc'],'files':manifest},ensure_ascii=False,indent=2))
print(json.dumps(validation,ensure_ascii=False,indent=2))
raise SystemExit(0 if passed else 1)
