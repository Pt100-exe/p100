"""CLI local para congelar/verificar esta contribución, sin acceder a la red."""

import argparse
import json
from pathlib import Path

from .freeze import build_manifest, verify_manifest, write_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("freeze", "verify"))
    parser.add_argument("--manifest", default="FREEZE_MANIFEST.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    destination = (root / args.manifest).resolve()
    if not destination.is_relative_to(root):
        parser.error("el manifiesto debe estar dentro de v06_foundations")
    if args.action == "freeze":
        config = json.loads((root / "config" / "example.json").read_text(encoding="utf-8"))
        code_files = [path.relative_to(root).as_posix() for folder in ("p100_foundations", "tests") for path in (root / folder).rglob("*.py")]
        code_files.append("config/example.json")
        manifest = build_manifest(root, code_files, [], config)
        write_manifest(destination, manifest)
        print(json.dumps({"status": "FROZEN_COMPONENT_BASELINE", "manifest_sha256": manifest["manifest_sha256"], "data_status": manifest["data_status"], "holdout_status": manifest["holdout_status"]}, sort_keys=True))
        return 0
    manifest = json.loads(destination.read_text(encoding="utf-8"))
    errors = verify_manifest(root, manifest)
    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, sort_keys=True))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
