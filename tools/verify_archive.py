#!/usr/bin/env python3
"""Verify downloadable release parts; optionally verify every tar member."""
from pathlib import Path, PurePosixPath
import argparse, gzip, hashlib, json, shutil, subprocess, tarfile, threading

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--directory', type=Path, required=True, help='Directory containing downloaded .partNNN files')
    ap.add_argument('--index', type=Path, default=Path(__file__).resolve().parents[1] / 'publication_index.json')
    ap.add_argument('--group', help='Verify only this archive group')
    ap.add_argument('--payload', action='store_true', help='Also decompress and check every archived file (requires zstd)')
    args = ap.parse_args()
    index = json.loads(args.index.read_text(encoding='utf-8'))
    groups = [g for g in index['groups'] if not args.group or g['group'] == args.group]
    if not groups:
        ap.error('Unknown archive group')
    for g in groups:
        for part in g['parts']:
            p = args.directory / part['name']
            h = hashlib.sha256()
            with p.open('rb') as f:
                for block in iter(lambda: f.read(4*1024*1024), b''):
                    h.update(block)
            if p.stat().st_size != part['bytes'] or h.hexdigest() != part['sha256']:
                raise RuntimeError('Part mismatch: ' + p.name)
        print(g['group'], 'part SHA256 PASS', flush=True)
        if not args.payload:
            continue
        if not shutil.which('zstd'):
            raise RuntimeError('Install zstd to use --payload')
        manifest = args.index.parent / g['manifest']
        expected = {}
        with gzip.open(manifest, 'rt', encoding='utf-8') as f:
            for line in f:
                x = json.loads(line)
                if x['path'] in expected:
                    raise RuntimeError('Duplicate manifest path')
                expected[x['path']] = x
        proc = subprocess.Popen(['zstd', '-dc', '--memory=512MB'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        pump_errors = []
        def pump():
            try:
                for part in g['parts']:
                    with (args.directory / part['name']).open('rb') as f:
                        shutil.copyfileobj(f, proc.stdin, 4*1024*1024)
            except BaseException as e:
                pump_errors.append(e)
            finally:
                proc.stdin.close()
        t = threading.Thread(target=pump, daemon=True)
        t.start()
        seen = set()
        try:
            with tarfile.open(fileobj=proc.stdout, mode='r|') as tar:
                for member in tar:
                    path = PurePosixPath(member.name)
                    if not member.isfile() or path.is_absolute() or '..' in path.parts:
                        raise RuntimeError('Unsafe/nonregular tar entry: ' + member.name)
                    if member.name not in expected or member.name in seen:
                        raise RuntimeError('Unexpected/duplicate entry: ' + member.name)
                    row = expected[member.name]
                    h = hashlib.sha256()
                    with tar.extractfile(member) as f:
                        for block in iter(lambda: f.read(1024*1024), b''):
                            h.update(block)
                    if member.size != row['bytes'] or h.hexdigest() != row['public_sha256']:
                        raise RuntimeError('Payload mismatch: ' + member.name)
                    seen.add(member.name)
            while proc.stdout.read(1024*1024):
                pass
            code = proc.wait()
            t.join()
            if code or pump_errors or seen != set(expected):
                raise RuntimeError('Incomplete archive or decompression failure')
        except BaseException:
            proc.kill()
            raise
        print(g['group'], str(len(seen)) + ' file SHA256 + zstd checksum PASS', flush=True)
    print('All requested checks PASS')

if __name__ == '__main__':
    main()
