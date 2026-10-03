#!/usr/bin/env python3
"""Small local validation runner; no packages, services, CI or browser downloads."""
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import shlex
import subprocess

root = Path(__file__).resolve().parents[1]
log = ['Local Soap presentation validation', datetime.now(timezone.utc).isoformat()]
commands = [
    ['taskset', '-c', '11', 'node', 'tests/live-models.mjs'],
    ['node', '--check', 'docs/live.js'],
    ['node', '--check', 'docs/live-model.js'],
]
for command in commands:
    completed = subprocess.run(command, cwd=root, capture_output=True, text=True)
    log += ['$ ' + shlex.join(command), completed.stdout.rstrip(), completed.stderr.rstrip(), 'exit=' + str(completed.returncode)]
    if completed.returncode:
        (root / 'validation/local-checks.txt').write_text('\n'.join(log) + '\n')
        raise SystemExit(completed.returncode)

class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'script' and attrs.get('src'):
            self.paths.append(attrs['src'])
        if tag == 'link' and attrs.get('rel') == 'stylesheet':
            self.paths.append(attrs['href'])

assets = Assets()
assets.feed((root / 'docs/live.html').read_text())
for asset in assets.paths:
    assert '://' not in asset and not asset.startswith('/'), asset
    assert (root / 'docs' / asset).is_file(), asset
log += ['Runtime script/style assets: all adjacent files exist; no remote dependencies.']
for engine in ['steiner.js', 'surface.js', 'film3d.js', 'filmcolor.js']:
    current = (root / 'docs' / engine).read_bytes()
    original = subprocess.check_output(['git', 'show', 'HEAD:docs/' + engine], cwd=root)
    assert current == original, engine + ' changed'
    log += [engine + ' unchanged; sha256=' + hashlib.sha256(current).hexdigest()]
log += ['PASS: local geometry, source syntax, runtime dependencies, unchanged numerical/rendering engines.', 'Not covered here: browser controls/rendered layout. The kit browser suite supplies that evidence.']
(root / 'validation').mkdir(exist_ok=True)
(root / 'validation/local-checks.txt').write_text('\n'.join(line for line in log if line) + '\n')
print('\n'.join(line for line in log if line))
