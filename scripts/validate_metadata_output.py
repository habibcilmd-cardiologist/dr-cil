#!/usr/bin/env python3
"""Verify emitted social/GSC/GA/sitemap metadata; no HTTP or account claims."""
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import struct
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta = {}
        self.canonical = []
        self.alias = False
        self.analytics = []
        self._analytics = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta':
            key = a.get('property', a.get('name', ''))
            self.meta.setdefault(key, []).append(a.get('content', ''))
            if a.get('http-equiv', '').lower() == 'refresh': self.alias = True
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical.append(a.get('href', ''))
        if tag == 'script' and a.get('id') == 'site-analytics':
            self.analytics.append('')
            self._analytics = True

    def handle_endtag(self, tag):
        if tag == 'script': self._analytics = False

    def handle_data(self, data):
        if self._analytics: self.analytics[-1] += data


def image_info(path):
    """Read raster magic bytes and dimensions without an imaging dependency."""
    data = path.read_bytes()
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png', *struct.unpack('>II', data[16:24])
    if data.startswith((b'GIF87a', b'GIF89a')):
        return 'image/gif', *struct.unpack('<HH', data[6:10])
    if data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        kind = data[12:16]
        if kind == b'VP8X':
            return 'image/webp', 1+int.from_bytes(data[24:27], 'little'), 1+int.from_bytes(data[27:30], 'little')
        if kind == b'VP8L':
            bits = int.from_bytes(data[21:25], 'little')
            return 'image/webp', 1+(bits & 0x3fff), 1+((bits >> 14) & 0x3fff)
        if kind == b'VP8 ':
            start = data.index(b'\x9d\x01\x2a', 20, 40) + 3
            width, height = struct.unpack('<HH', data[start:start+4])
            return 'image/webp', width & 0x3fff, height & 0x3fff
    if data.startswith(b'\xff\xd8'):
        position = 2
        while position < len(data):
            if data[position] != 255: raise ValueError('Invalid JPEG marker')
            while data[position] == 255: position += 1
            marker = data[position]; position += 1
            length = int.from_bytes(data[position:position+2], 'big')
            if marker in {0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf}:
                height, width = struct.unpack('>HH', data[position+3:position+7])
                return 'image/jpeg', width, height
            position += length
    raise ValueError('Unsupported or invalid raster image')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('public', type=Path)
    ap.add_argument('--source', type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument('--json', type=Path)
    args = ap.parse_args()
    config = (args.source/'hugo.toml').read_text()
    base_url = re.search(r'^baseURL\s*=\s*"([^"]+)"', config, re.M).group(1)
    origin = urlsplit(base_url)
    verification = re.search(r'^\s*google\s*=\s*"([^"]+)"', config, re.M).group(1)
    analytics_source = (args.source/'layouts/partials/extend-head-uncached.html').read_text()
    measurement = re.search(r'gtag\("config",\s*"([^"]+)"\)', analytics_source).group(1)
    counts = Counter(); cards = Counter(); errors = []; images = {}; examples = {}

    def fail(file, code, detail):
        errors.append({'file':str(file), 'code':code, 'detail':detail})

    for file in sorted(args.public.rglob('*.html')):
        counts['html'] += 1
        doc = Document(); doc.feed(file.read_text())
        rel = file.relative_to(args.public).as_posix()
        if doc.alias:
            counts['aliases'] += 1
            continue
        counts['pages_checked'] += 1
        for key in ['og:title','og:type','og:url','og:description','og:site_name','og:locale',
                    'og:image','og:image:type','og:image:width','og:image:height','og:image:alt',
                    'twitter:title','twitter:description','twitter:image','twitter:image:alt','twitter:card']:
            values = doc.meta.get(key, [])
            if len(values) != 1 or not values[0]: fail(rel, 'SOCIAL_MISSING_OR_DUPLICATE', key)
        def value(key): return (doc.meta.get(key) or [''])[0]
        if doc.canonical != [value('og:url')]: fail(rel, 'SOCIAL_CANONICAL', doc.canonical)
        canonical = urlsplit(value('og:url'))
        if (canonical.scheme, canonical.netloc) != (origin.scheme, origin.netloc): fail(rel,'PRODUCTION_ORIGIN',value('og:url'))
        if doc.meta.get('google-site-verification') != [verification]: fail(rel,'GSC_TOKEN',doc.meta.get('google-site-verification'))
        if len(doc.analytics) != 1 or doc.analytics[0].count(measurement) != 2: fail(rel,'GA_ID_OR_DUPLICATE',len(doc.analytics))
        image = value('og:image'); image_url = urlsplit(image)
        if image != value('twitter:image'): fail(rel,'TWITTER_IMAGE_MISMATCH',value('twitter:image'))
        if (image_url.scheme,image_url.netloc) != (origin.scheme,origin.netloc): fail(rel,'IMAGE_ORIGIN',image)
        image_path = args.public/unquote(image_url.path).lstrip('/')
        try:
            if image not in images: images[image] = image_info(image_path)
            mime,width,height = images[image]
            declared = (value('og:image:type'),value('og:image:width'),value('og:image:height'))
            if declared != (mime,str(width),str(height)): fail(rel,'IMAGE_METADATA',{'actual':[mime,width,height],'declared':declared})
            expected_card = 'summary_large_image' if width/height >= 1.5 else 'summary'
            if value('twitter:card') != expected_card: fail(rel,'TWITTER_CARD_ASPECT',value('twitter:card'))
        except (OSError,ValueError,IndexError,struct.error) as exc:
            fail(rel,'IMAGE_FILE',str(exc))
        cards[value('twitter:card')] += 1
        for key in ['index.html','en/index.html','ar/index.html','blog/diyabetik-ayak/index.html','hizmetler/dizalti-damar-tikanikligi/index.html']:
            if rel == key: examples[rel] = {'canonical':doc.canonical,'image':image,'card':value('twitter:card'),'gsc':doc.meta.get('google-site-verification'),'analytics_scripts':len(doc.analytics)}

    robots = (args.public/'robots.txt').read_text()
    maps = {}
    ns = {'sm':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    for relative in ['sitemap.xml','en/sitemap.xml','ar/sitemap.xml']:
        url = base_url.rstrip('/')+'/'+relative
        if 'Sitemap: '+url not in robots: fail('robots.txt','SITEMAP_NOT_DECLARED',url)
        try:
            tree = ET.parse(args.public/relative)
            locs = [(node.text or '') for node in tree.findall('.//sm:loc',ns)]
            if not locs: fail(relative,'SITEMAP_EMPTY',None)
            for loc in locs:
                parsed = urlsplit(loc)
                if (parsed.scheme,parsed.netloc)!=(origin.scheme,origin.netloc): fail(relative,'SITEMAP_ORIGIN',loc)
            maps[relative] = len(locs)
        except (OSError,ET.ParseError) as exc: fail(relative,'SITEMAP_XML',str(exc))
    result = {'scope':'Emitted social metadata, image bytes/dimensions, GSC token, GA code and sitemap/robots; not HTTP, account ownership, live Analytics collection or external preview acceptance',
              'public':str(args.public),'counts':dict(counts),'twitter_cards':dict(cards),'image_assets':{key:list(value) for key,value in images.items()},
              'sitemaps':maps,'measurement_id':measurement,'examples':examples,'error_count':len(errors),'errors':errors,
              'google_faq_rich_result':'REMOVED_BY_GOOGLE_2026-05-07','runtime_guard':'Run scripts/tests/analytics-guard.test.mjs separately with mocked document; no requests'}
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({key:value for key,value in result.items() if key not in {'errors','examples'}},ensure_ascii=False,indent=2))
    return int(bool(errors))


if __name__ == '__main__': raise SystemExit(main())
