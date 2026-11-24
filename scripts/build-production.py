#!/usr/bin/env python3
"""Build a fresh release directory without cleaning public or source resources."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='New/empty release directory; output is inside public/')
    parser.add_argument('--baseURL', help='Explicit alternate baseURL for an isolated build')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    release = args.output.resolve() if args.output else Path(tempfile.mkdtemp(prefix='dr-cil-production-'))
    if release.exists() and any(release.iterdir()):
        parser.error('--output must be a new or empty directory; existing files will not be removed')
    release.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(HUGO_RESOURCEDIR=str(release / 'resources'), HUGO_CACHEDIR=str(release / 'cache'))
    command = ['hugo', '--environment', 'production', '--minify', '--noBuildLock',
               '--destination', str(release / 'public'), '--cacheDir', str(release / 'cache')]
    if args.baseURL:
        command.extend(['--baseURL', args.baseURL])
    version = subprocess.check_output(['hugo', 'version'], cwd=root, text=True).strip()
    expected = (root / 'hugo-version.txt').read_text().strip()
    if not version.startswith('hugo v' + expected + '+') or 'extended' not in version:
        parser.error('This release requires Hugo Extended ' + expected + '; actual: ' + version)
    result = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True)
    (release / 'build.log').write_text(result.stdout + result.stderr)
    manifest = {'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'hugo': version, 'command': command, 'exit_code': result.returncode,
                'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
                'public': str(release / 'public'), 'files': {}}
    if result.returncode == 0:
        for p in sorted((release / 'public').rglob('*')):
            if p.is_file():
                manifest['files'][p.relative_to(release / 'public').as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    (release / 'build-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(result.stdout, end='')
    print(result.stderr, end='', file=sys.stderr)
    print(json.dumps({'exit_code': result.returncode, 'release': str(release), 'public': manifest['public']}))
    return result.returncode

if __name__ == '__main__':
    raise SystemExit(main())
