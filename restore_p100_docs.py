from pathlib import Path
import hashlib
import json
import zipfile
root = Path(__file__).resolve().parents[1]
archive = root/'P100_Transferencia_Codex_2026-09-07.zip'
assert hashlib.sha256(archive.read_bytes()).hexdigest() == '6e17b4635914d600c3aaccc9497e22d9f5dbca7f2a88ba119aa77f79302fe2c9'
manifest = json.loads((root/'P100_TRANSFER/MANIFEST_SHA256.json').read_text(encoding='utf-8'))
with zipfile.ZipFile(archive) as z:
    for name in ('04_DOCUMENTO/P100_Documento_integral.md', '04_DOCUMENTO/P100_Documento_integral.pdf'):
        match = [n for n in z.namelist() if n.endswith('/'+name) or n==name]
        assert len(match)==1
        data = z.read(match[0])
        record = next(r for r in manifest['files'] if r['path']==name)
        assert hashlib.sha256(data).hexdigest() == record['sha256']
        target = root/'P100_TRANSFER'/name
        assert target.resolve().is_relative_to((root/'P100_TRANSFER').resolve())
        with target.open('xb') as f:
            f.write(data)
        print('Restaurado con hash original:', name)
