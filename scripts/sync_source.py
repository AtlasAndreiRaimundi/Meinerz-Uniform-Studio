#!/usr/bin/env python3
"""Import a fresh authorized Sites checkout, never credentials or Git history."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if len(sys.argv) != 2:
    raise SystemExit('Usage: python3 scripts/sync_source.py /authorized/sites/checkout')
checkout = Path(sys.argv[1]).resolve()
sha = subprocess.check_output(['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip()
hosting = json.loads(subprocess.check_output(['git', '-C', str(checkout), 'show', sha + ':.openai/hosting.json']))
if hosting['project_id'] != 'appgprj_6ad921f302148191932d8c1e12374ce3':
    raise SystemExit('Wrong Sites project')
entries = subprocess.check_output(['git', '-C', str(checkout), 'ls-tree', '-r', '-z', sha]).split(b'\0')[:-1]
objects = []
for entry in entries:
    metadata, raw_name = entry.split(b'\t', 1)
    mode, kind, object_sha = metadata.split()
    if kind != b'blob' or mode not in {b'100644', b'100755'}:
        raise SystemExit('Unsupported source entry; review before exporting')
    objects.append((raw_name.decode('utf-8'), object_sha, mode.decode('ascii')))
with tempfile.TemporaryDirectory() as temp:
    stage = Path(temp)
    (stage / 'scripts').mkdir()
    shutil.copy2(ROOT / 'scripts/check_source.py', stage / 'scripts/check_source.py')
    files = []
    reader = subprocess.Popen(['git', '-C', str(checkout), 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    for name, object_sha, mode in objects:
        path = Path(name)
        if path.is_absolute() or '..' in path.parts:
            raise SystemExit('Unsafe source path')
        reader.stdin.write(object_sha + b'\n')
        reader.stdin.flush()
        header = reader.stdout.readline().split()
        if len(header) != 3 or header[0] != object_sha or header[1] != b'blob':
            reader.kill()
            raise SystemExit('Unexpected Git object response')
        size = int(header[2])
        data = reader.stdout.read(size)
        if len(data) != size or reader.stdout.read(1) != b'\n':
            reader.kill()
            raise SystemExit('Incomplete Git object response')
        target = stage / 'source' / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(0o755 if mode == '100755' else 0o644)
        files.append({'path': name, 'mode': mode, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    reader.stdin.close()
    reader.stdout.close()
    if reader.wait() != 0:
        raise SystemExit('Git object export failed')
    subprocess.run([sys.executable, str(stage / 'scripts/check_source.py')], check=True)
    # Scan completes before replacing the previous snapshot. Git preserves deletions.
    if (ROOT / 'source').exists():
        shutil.rmtree(ROOT / 'source')
    shutil.copytree(stage / 'source', ROOT / 'source')
manifest = {'project_id': hosting['project_id'], 'source_commit': sha, 'exported_at': datetime.now(timezone.utc).isoformat(), 'files': files}
(ROOT / 'source-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print('Imported', len(files), 'files from', sha)
print('Review git diff, run checks, update CHANGELOG, commit and push without force.')
