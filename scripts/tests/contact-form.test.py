#!/usr/bin/env python3
"""Render real shortcode modes in isolated Hugo fixtures; never send a POST."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.forms = []
        self.fallbacks = 0
        self.labels = set()
        self.fields = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'form': self.forms.append(a)
        if 'data-contact-fallback' in a: self.fallbacks += 1
        if tag == 'label': self.labels.add(a.get('for'))
        if tag in ('input', 'textarea') and a.get('type') != 'hidden' and a.get('name') != 'bot-field':
            self.fields.append(a)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[2]
    cases = [
        ('disabled', 'disabled', '', False),
        ('missing-endpoint', 'endpoint', '', False),
        ('relative-endpoint', 'endpoint', '/messages/receive/', True),
        ('https-endpoint', 'endpoint', 'https://forms.example.invalid/receive', True),
        ('unsafe-scheme', 'endpoint', 'javascript:alert(1)', False),
        ('protocol-relative', 'endpoint', '//forms.example.invalid/receive', False),
        ('netlify', 'netlify', '', True),
        ('unknown-provider', 'not-selected', '/messages/receive/', False),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix='drcil-contact-test-') as temp:
        for name, provider, endpoint, render_form in cases:
            site = Path(temp) / name
            shortcode = site/'layouts/shortcodes/contact-form.html'
            shortcode.parent.mkdir(parents=True)
            shutil.copyfile(root/'layouts/shortcodes/contact-form.html', shortcode)
            (site/'layouts/index.html').write_text('<!doctype html><html lang="{{ .Language.Lang }}"><body>{{ .Content }}</body></html>')
            config = 'baseURL = "https://example.invalid/"\ndefaultContentLanguage = "tr"\n[params.contactForm]\nprovider = '+json.dumps(provider)+'\nendpoint = '+json.dumps(endpoint)+'\n'
            for lang in ('tr','en','ar'):
                folder = site/'content'/lang
                folder.mkdir(parents=True)
                (folder/'_index.md').write_text('---\ntitle: Contact fixture\n---\n{{< contact-form success="/thanks/" >}}\n')
                config += '\n[languages.'+lang+']\ncontentDir = "content/'+lang+'"\n'
            (site/'hugo.toml').write_text(config)
            command = ['hugo','--source',str(site),'--destination',str(site/'public'),'--noBuildLock','--quiet']
            build = subprocess.run(command, capture_output=True, text=True, timeout=30)
            errors = []
            if build.returncode:
                errors.append(build.stderr)
            else:
                for lang in ('tr','en','ar'):
                    file = site/'public'/('' if lang=='tr' else lang)/'index.html'
                    page = Page(); page.feed(file.read_text())
                    if len(page.forms) != int(render_form): errors.append(lang+': form gating failed')
                    if not render_form and page.fallbacks != 1: errors.append(lang+': real contact fallback missing')
                    if render_form and page.forms:
                        form = page.forms[0]
                        expected = '/thanks/' if provider=='netlify' else endpoint
                        if form.get('method') != 'POST' or form.get('action') != expected: errors.append(lang+': method/action mismatch')
                        if ('data-netlify' in form) != (provider=='netlify'): errors.append(lang+': provider attributes leaked')
                        if len(page.fields)!=4 or any(x.get('id') not in page.labels for x in page.fields): errors.append(lang+': accessible field labels missing')
            results.append({'case':name,'languages':3,'exit_code':build.returncode,'errors':errors,'pass':not errors})
    report = {'scope':'Real Hugo rendering of shortcode; no HTTP or form delivery test','cases':results,'passed':sum(x['pass'] for x in results),'failed':sum(not x['pass'] for x in results)}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False))
    return int(bool(report['failed']))

if __name__=='__main__':
    raise SystemExit(main())
