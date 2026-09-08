"""Verifica la copia completa y opcionalmente ejecuta pruebas sin red."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--pruebas',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'CONTENIDO_SHA256.json').read_text(encoding='utf-8'))
    errors=[]
    for entry in manifest['files']:
        p=(root/entry['path']).resolve()
        if not p.is_relative_to(root) or not p.is_file():
            errors.append(entry['path']+': missing or unsafe')
        elif p.stat().st_size!=entry['bytes'] or digest(p)!=entry['sha256']:
            errors.append(entry['path']+': mismatch')
    print(json.dumps(dict(status='FAIL' if errors else 'PASS',checked=len(manifest['files']),errors=errors),ensure_ascii=False))
    if errors:
        return 1
    if args.pruebas:
        commands=[('P100_TRANSFER',['06_VERIFICACION/verify_package.py']),
                  ('P100_LAB',['verify_delivery.py']),
                  ('P100_RESEARCH',['verify_delivery.py']),
                  ('P100_RESEARCH',['audit_study.py']),
                  ('P100_RESEARCH',['-m','unittest','discover','-s','tests','-v'])]
        for folder,arguments in commands:
            print('CHECK '+folder+' '+' '.join(arguments),flush=True)
            result=subprocess.run([sys.executable,'-B',*arguments],cwd=root/folder)
            if result.returncode:
                return result.returncode
    return 0

if __name__=='__main__':
    raise SystemExit(main())
