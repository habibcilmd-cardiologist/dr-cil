"""Offline before/after artifact inventory. File bytes are not HTTP transfer timings."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.images=[]; self.scripts=[]; self.viewers=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='img' and 'home-hero-image' in a.get('class','').split():self.images.append(a)
        if tag=='script':self.scripts.append(a)
        if 'data-heart-model' in a:self.viewers.append(a)

def inspect(root):
    root=Path(root); pages={}; model_name='3d-kalp-modeli-doc-dr-habib-cil-istanbul-kardiyoloji-uzmani.glb'
    for rel in ['index.html','en/index.html','ar/index.html']:
        f=root/rel;p=Page();p.feed(f.read_text()); scripts=[]
        for a in p.scripts:
            src=a.get('src','');u=urlsplit(src)
            local=root/unquote(u.path).lstrip('/')
            scripts.append({'src':src,'type':a.get('type',''),'defer':'defer'in a,'async':'async'in a,'file_bytes':local.stat().st_size if src and (not u.hostname or u.hostname=='docdrhabibcil.com') and local.is_file() else None})
        pages[rel]={'html_bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'hero_images':p.images,'scripts':scripts,'viewer_count':len(p.viewers),'viewer_data':p.viewers}
    model=root/'models'/model_name;poster=root/'img/anatomical-heart-diagram.svg'
    return {'root':str(root),'html_files':len(list(root.rglob('*.html'))),'pages':pages,'active_model':{'bytes':model.stat().st_size,'sha256':hashlib.sha256(model.read_bytes()).hexdigest()},'poster':{'bytes':poster.stat().st_size,'sha256':hashlib.sha256(poster.read_bytes()).hexdigest()}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--before',required=True);ap.add_argument('--after');ap.add_argument('--output',required=True);a=ap.parse_args()
    data={'date_utc':datetime.now(timezone.utc).isoformat(),'type':'offline artifact inventory only; no HTTP, browser or performance score','before':inspect(a.before),'after':inspect(a.after) if a.after else None,'runtime_metrics':None}
    Path(a.output).write_text(json.dumps(data,ensure_ascii=False,indent=2));print(json.dumps({'before_html':data['before']['html_files'],'after_html':data['after']['html_files'] if data['after'] else None,'runtime_metrics':None}))
