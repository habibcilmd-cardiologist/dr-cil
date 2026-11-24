"""Offline payload audit. No requests, server, browser or source edits.

Run from repository root:
python3 docs/audit/results/2026-11-24/evidence/performance-collect.py
"""
import csv
import gzip
import hashlib
import json
import struct
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path('/tmp/dr-cil-audit-2026-11-24/public')
OUT = Path(__file__).parent


def file_info(path):
    data = path.read_bytes()
    return {'bytes': len(data),
            'gzip9_estimate_bytes': len(gzip.compress(data, compresslevel=9, mtime=0)),
            'sha256': hashlib.sha256(data).hexdigest()}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts, self.links, self.images, self.videos, self.styles = [], [], [], [], []
        self.script, self.style = None, None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'script':
            self.script = {'attrs': attrs, 'body': ''}
            self.scripts.append(self.script)
        if tag == 'style':
            self.style = ''
        if tag == 'link':
            self.links.append(attrs)
        if tag == 'img':
            self.images.append(attrs)
        if tag in ('video', 'source'):
            self.videos.append(attrs)

    def handle_data(self, data):
        if self.script is not None:
            self.script['body'] += data
        if self.style is not None:
            self.style += data

    def handle_endtag(self, tag):
        if tag == 'script':
            self.script = None
        if tag == 'style':
            self.styles.append(self.style or '')
            self.style = None


result = {'date': '2026-11-24',
          'method': 'Offline production output inspection only; gzip9 is a size estimate, not HTTP transfer or negotiated encoding; no timing metrics.',
          'pages': {}, 'models': {}, 'source_assets': {},
          'all_html_3d_paths': {'active_partial_model': [], 'eager_shortcode_model': [], 'video_tags': []}}
rows = []
samples = ['index.html', 'en/index.html', 'ar/index.html',
           'hizmetler/dizalti-damar-tikanikligi/index.html',
           'hizmetler/periferik-damar/index.html', 'blog/diyabetik-ayak/index.html']
for name in samples:
    path = ROOT / name
    if not path.is_file():
        continue
    parser = PageParser()
    parser.feed(path.read_text())
    entry = {'html': file_info(path), 'scripts': [], 'stylesheets': [],
             'hero_images': [x for x in parser.images if 'home-hero-image' in x.get('class', '')],
             'image_count': len(parser.images), 'video_tags': parser.videos,
             'inline_executable_script_bytes': 0,
             'inline_style_bytes': sum(len(x.encode()) for x in parser.styles)}
    for script in parser.scripts:
        attrs, body = script['attrs'], script['body']
        item = {'attributes': attrs}
        if attrs.get('src'):
            url = urlsplit(attrs['src'])
            target = ROOT / unquote(url.path).lstrip('/')
            if (not url.netloc or url.hostname in ('docdrhabibcil.com', 'localhost')) and target.is_file():
                item.update(file_info(target))
                rows.append([name, 'script', url.path, item['bytes'], item['gzip9_estimate_bytes'], item['sha256']])
            else:
                item['external'] = True
        else:
            item['inline_bytes'] = len(body.encode())
            item['contains_3d_lazy_init'] = 'requestIdleCallback' in body and '3d-kalp-modeli-doc-dr-habib-cil-istanbul-kardiyoloji-uzmani.glb' in body
            if attrs.get('type') != 'application/ld+json':
                entry['inline_executable_script_bytes'] += item['inline_bytes']
        entry['scripts'].append(item)
    for attrs in parser.links:
        if attrs.get('rel') != 'stylesheet':
            continue
        url = urlsplit(attrs['href'])
        target = ROOT / unquote(url.path).lstrip('/')
        item = {'attributes': attrs}
        if target.is_file():
            item.update(file_info(target))
            rows.append([name, 'stylesheet', url.path, item['bytes'], item['gzip9_estimate_bytes'], item['sha256']])
        entry['stylesheets'].append(item)
    for image in entry['hero_images']:
        target = ROOT / unquote(urlsplit(image['src']).path).lstrip('/')
        if target.is_file():
            image['file'] = file_info(target)
            rows.append([name, 'hero_image', image['src'], image['file']['bytes'], image['file']['gzip9_estimate_bytes'], image['file']['sha256']])
    index_path = path.parent / 'index.json'
    if index_path.is_file():
        entry['search_index'] = file_info(index_path)
    result['pages'][name] = entry

for path in (ROOT / 'models').iterdir():
    if path.is_file():
        result['models'][path.name] = file_info(path)
for name in ['assets/css/custom.css', 'themes/blowfish/assets/css/compiled/main.css',
             'assets/videos/istanbul-kardiyolog-doc-dr-habib-cil-anjiyoplasti.mp4']:
    result['source_assets'][name] = file_info(Path(name))
for path in ROOT.rglob('*.html'):
    html = path.read_text()
    name = str(path.relative_to(ROOT))
    if '3d-kalp-modeli-doc-dr-habib-cil-istanbul-kardiyoloji-uzmani.glb' in html:
        result['all_html_3d_paths']['active_partial_model'].append(name)
    if 'istanbul-kardiyolog-dr-habib-cil.glb' in html:
        result['all_html_3d_paths']['eager_shortcode_model'].append(name)
    if '<video' in html:
        result['all_html_3d_paths']['video_tags'].append(name)

(OUT / 'performance-asset-inventory.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
with (OUT / 'performance-asset-inventory.csv').open('w') as file:
    writer = csv.writer(file)
    writer.writerow(['page', 'kind', 'url', 'bytes_offline', 'gzip9_estimate_bytes', 'sha256'])
    writer.writerows(rows)
print('Offline performance inventory written; no HTTP or browser measurements performed.')
