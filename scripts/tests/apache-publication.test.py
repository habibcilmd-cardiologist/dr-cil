#!/usr/bin/env python3
"""Exercise the actual .htaccess in an isolated Apache fixture; no external HTTP."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import pwd
import grp
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--port', type=int, default=1316)
    ap.add_argument('--httpd', default='/usr/sbin/httpd')
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[2]
    work = Path(tempfile.mkdtemp(prefix='dr-cil-apache-acceptance-'))
    public = work / 'public'
    public.mkdir()
    fixture = {
        'index.html': 'TR_HOME ' + ('content ' * 2000),
        'en/index.html': 'EN_HOME', 'ar/index.html': 'AR_HOME',
        '404.html': 'TR_NOT_FOUND', 'en/404.html': 'EN_NOT_FOUND',
        'ar/404.html': 'AR_NOT_FOUND', 'hizmetler/index.html': 'SERVICES',
        'sitemap.xml': '<urlset/>', 'en/sitemap.xml': '<urlset/>',
        'ar/sitemap.xml': '<urlset/>', 'robots.txt': 'User-agent: *\nAllow: /\n',
        'index.json': '[]', 'css/site.css': 'body {color: black}',
        'css/site.' + ('a' * 64) + '.css': 'body {color: black}',
        'models/heart.glb': 'GLB_FIXTURE',
        'blog/işlem/index.html': 'UNICODE_TR',
        'tags/اختبار/index.html': 'UNICODE_AR',
        'blog/part#one/index.html': 'ENCODED_HASH',
        '.well-known/acme-challenge/probe': 'ACME_PROBE',
        'hugo.toml': 'SOURCE_MUST_NOT_BE_PUBLIC',
    }
    for name, content in fixture.items():
        file = public / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content)
    shutil.copyfile(root / 'static/.htaccess', public / '.htaccess')
    tests = []

    def check(name, success, detail=None):
        tests.append({'name': name, 'pass': bool(success), 'detail': detail})

    check('source_root_and_static_mirror', (root / '.htaccess').read_bytes() == (public / '.htaccess').read_bytes())
    modules = ['mpm_prefork', 'unixd', 'authz_core', 'authz_host', 'dir',
               'mime', 'rewrite', 'headers', 'filter', 'deflate']
    config = '\n'.join([
        'ServerRoot "' + str(work) + '"',
        *['LoadModule ' + name + '_module /usr/libexec/apache2/mod_' + name + '.so' for name in modules],
        'Listen 127.0.0.1:' + str(args.port), 'ServerName localhost',
        'PidFile "' + str(work / 'httpd.pid') + '"',
        'ErrorLog "' + str(work / 'error.log') + '"',
        'User ' + pwd.getpwuid(os.getuid()).pw_name,
        'Group ' + grp.getgrgid(os.getgid()).gr_name,
        'TypesConfig /etc/apache2/mime.types',
        'DocumentRoot "' + str(public) + '"',
        '<Directory "' + str(public) + '">',
        'Options FollowSymLinks', 'AllowOverride All', 'Require all granted',
        '</Directory>', '',
    ])
    config_file = work / 'httpd.conf'
    config_file.write_text(config)
    syntax_file = work / 'syntax-httpd.conf'
    syntax_file.write_text(config.replace('</Directory>', 'Include "' + str(public / '.htaccess') + '"\n</Directory>'))
    syntax = subprocess.run([args.httpd, '-t', '-f', str(syntax_file)], capture_output=True, text=True)
    (work / 'syntax.log').write_text(syntax.stdout + syntax.stderr)
    check('apache_syntax_with_actual_rules_in_directory_context', syntax.returncode == 0, syntax.stdout + syntax.stderr)
    report = {'scope': 'Isolated Apache fixture, actual .htaccess; not live host/TLS/CDN/PHP/form delivery',
              'work': str(work), 'public': str(public), 'config': str(config_file),
              'source_sha256': hashlib.sha256((public / '.htaccess').read_bytes()).hexdigest(),
              'port': args.port, 'http_acceptance': 'NOT_RUN', 'tests': tests}
    process = None
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())

    def get(path, headers=None):
        request = urllib.request.Request('http://127.0.0.1:' + str(args.port) + path,
                                         headers={'Host': 'localhost:' + str(args.port), **(headers or {})})
        try:
            response = opener.open(request, timeout=3)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            return response.status, dict(response.headers.items()), response.read()

    try:
        if syntax.returncode == 0:
            log = open(work / 'startup.log', 'w')
            # Apache shutdown can signal its process group; isolate the fixture
            # so terminating it cannot terminate this test runner or user tasks.
            process = subprocess.Popen([args.httpd, '-f', str(config_file), '-DFOREGROUND'], stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            ready = False
            for attempt in range(30):
                if process.poll() is not None:
                    break
                try:
                    status, _, _ = get('/')
                    if status == 200:
                        ready = True
                        break
                except (OSError, urllib.error.URLError):
                    pass
                time.sleep(0.1)
            check('isolated_apache_listener_ready', ready,
                  {'port': args.port, 'process_exit_code': process.poll()})
            if not ready:
                report['blocker'] = 'Apache listener did not become usable; no alternative port/API attempted.'
            else:
                report['http_acceptance'] = 'RUN'
                for route, marker in [('/', 'TR_HOME'), ('/en/', 'EN_HOME'), ('/ar/', 'AR_HOME'), ('/hizmetler/', 'SERVICES')]:
                    status, headers, body = get(route)
                    check('directory_index_' + route, status == 200 and marker.encode() in body, {'status': status})
                query = 'utm_source=apache-test&term=%C4%B0stanbul'
                for line in (root / 'static/_redirects').read_text().splitlines():
                    parts = line.split()
                    if len(parts) < 3 or parts[0].startswith('#') or '*' in parts[0] or not parts[2].startswith('301'):
                        continue
                    status, headers, _ = get(parts[0] + '?' + query)
                    target = urllib.parse.urlsplit(headers.get('Location', ''))
                    check('exact_301_' + parts[0], status == 301 and target.netloc == 'localhost:' + str(args.port)
                          and target.path == parts[1] and target.query == query,
                          {'status': status, 'location': headers.get('Location')})
                for source, target in [('/tr/', '/'), ('/tr/hizmetler/', '/hizmetler/'),
                                       ('/tr/blog/i%C5%9Flem/', '/blog/i%C5%9Flem/'),
                                       ('/tr/tags/%D8%A7%D8%AE%D8%AA%D8%A8%D8%A7%D8%B1/', '/tags/%D8%A7%D8%AE%D8%AA%D8%A8%D8%A7%D8%B1/'),
                                       ('/tr/blog/part%23one/', '/blog/part%23one/')]:
                    status, headers, _ = get(source + '?' + query)
                    location = urllib.parse.urlsplit(headers.get('Location', ''))
                    check('legacy_encoded_' + source, status == 301 and location.path == target and location.query == query,
                          {'status': status, 'location': headers.get('Location')})
                for source, target in [('/tr/page/2/', '/'), ('/en/page/4/', '/en/'), ('/tr/hizmetler/', '/hizmetler/'), ('/hizmetler/', '/hizmetler/')]:
                    status, headers, _ = get(source + '?' + query, {'Host': 'www.docdrhabibcil.com'})
                    check('production_one_hop_' + source, status == 301 and headers.get('Location') == 'https://docdrhabibcil.com' + target + '?' + query,
                          {'status': status, 'location': headers.get('Location')})
                for route, marker in [('/not-found/', 'TR_NOT_FOUND'), ('/en/not-found/', 'EN_NOT_FOUND'), ('/ar/not-found/', 'AR_NOT_FOUND')]:
                    status, headers, body = get(route)
                    check('localized_true_404_' + route, status == 404 and marker.encode() in body,
                          {'status': status, 'body': body.decode(), 'cache': headers.get('Cache-Control')})
                    check('error_not_cached_' + route, headers.get('Cache-Control') == 'no-store', headers)
                for route in ['/index.json', '/sitemap.xml', '/en/sitemap.xml', '/ar/sitemap.xml', '/robots.txt']:
                    status, headers, _ = get(route)
                    check('revalidation_' + route, status == 200 and headers.get('Cache-Control') == 'public, max-age=0, must-revalidate', headers)
                for route, mime in [('/models/heart.glb', 'model/gltf-binary'), ('/sitemap.xml', 'application/xml'), ('/index.json', 'application/json')]:
                    status, headers, _ = get(route)
                    check('mime_' + route, status == 200 and headers.get('Content-Type', '').startswith(mime), headers)
                for route, expected in [('/css/site.css', 'public, max-age=86400, must-revalidate'), ('/css/site.' + 'a' * 64 + '.css', 'public, max-age=31536000, immutable')]:
                    status, headers, _ = get(route)
                    check('asset_cache_' + route, status == 200 and headers.get('Cache-Control') == expected, headers)
                status, headers, _ = get('/css/missing.' + 'b' * 64 + '.css')
                check('missing_hash_asset_uncached_404', status == 404 and headers.get('Cache-Control') == 'no-store', headers)
                status, headers, body = get('/', {'Accept-Encoding': 'gzip'})
                check('gzip_and_vary', status == 200 and headers.get('Content-Encoding') == 'gzip'
                      and 'accept-encoding' in headers.get('Vary', '').lower()
                      and b'TR_HOME' in gzip.decompress(body), headers)
                status, headers, _ = get('/')
                check('security_headers', headers.get('X-Content-Type-Options') == 'nosniff'
                      and headers.get('X-Frame-Options') == 'DENY'
                      and headers.get('Referrer-Policy') == 'strict-origin-when-cross-origin', headers)
                etag = headers.get('ETag')
                status, headers, _ = get('/', {'If-None-Match': etag or ''})
                check('etag_conditional_304', etag and status == 304, {'status': status, 'headers': headers})
                for route in ['/.htaccess', '/hugo.toml']:
                    status, _, _ = get(route)
                    check('source_denied_' + route, status == 403, status)
                status, _, body = get('/.well-known/acme-challenge/probe')
                check('acme_allowed', status == 200 and body == b'ACME_PROBE', status)
    except Exception as error:
        check('unexpected_test_exception', False, repr(error))
    finally:
        if process is not None:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
            report['server_exit_code'] = process.returncode
        for name in ['error.log', 'startup.log']:
            file = work / name
            if file.exists():
                report[name] = file.read_text()
        report['passed'] = sum(item['pass'] for item in tests)
        report['failed'] = sum(not item['pass'] for item in tests)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps({'output': str(args.output), 'work': str(work), 'http_acceptance': report['http_acceptance'],
                          'passed': report['passed'], 'failed': report['failed'], 'blocker': report.get('blocker')}, ensure_ascii=False))
    return int(bool(report['failed']))


if __name__ == '__main__':
    raise SystemExit(main())
