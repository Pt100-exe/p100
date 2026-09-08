import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
manifest=json.loads((root/"MANIFEST.json").read_text())
errors=[]
for name,value in manifest["files"].items():
    p=root/name
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=value:
        errors.append(name)
print(json.dumps(dict(status="FAIL" if errors else "PASS",checked=len(manifest["files"]),errors=errors)))
raise SystemExit(bool(errors))
