"""Manifiesto determinista SHA-256 de archivos y configuración."""

import hashlib
import json
from pathlib import Path
from typing import Iterable, Mapping

from .registry import BURNED_RECORD, EvaluationWindow, candidate_holdout_status


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_records(root: Path, relative_paths: Iterable[str]) -> list[dict]:
    root = root.resolve(strict=True)
    records, seen = [], set()
    for name in sorted(relative_paths):
        path = (root / name).resolve(strict=True)
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError(f"archivo fuera del root o inválido: {name}")
        relative = path.relative_to(root).as_posix()
        if relative in seen:
            raise ValueError(f"archivo duplicado: {relative}")
        seen.add(relative)
        content = path.read_bytes()
        records.append({"path": relative, "bytes": len(content), "sha256": digest(content)})
    return sorted(records, key=lambda record: record["path"])


def build_manifest(root: Path, code_files: Iterable[str], data_files: Iterable[str], config: Mapping, *, candidate_holdout: EvaluationWindow | None = None) -> dict:
    config_copy = json.loads(canonical_bytes(dict(config)))
    code = file_records(root, code_files)
    data = file_records(root, data_files)
    if not code:
        raise ValueError("el manifiesto exige al menos un archivo de código")
    payload = {
        "schema": "p100-foundations-freeze-1",
        "implementation_origin": "NEW_INDEPENDENT_COMPONENTS_NOT_RECOVERED_V05",
        "code": code,
        "data": data,
        "data_status": "FILES_HASHED_CONTENT_NOT_AUDITED" if data else "NO_MARKET_DATA_PROVIDED",
        "config": config_copy,
        "config_sha256": digest(canonical_bytes(config_copy)),
        "burned_evaluation": dict(BURNED_RECORD),
        "holdout_status": candidate_holdout_status(candidate_holdout),
        "candidate_holdout": None if candidate_holdout is None else {
            "start_inclusive": candidate_holdout.start.isoformat(),
            "end_exclusive": candidate_holdout.end.isoformat(),
        },
        "scope": "Identidad de bytes y parámetros; no prueba disponibilidad temporal, autenticidad ni rendimiento.",
    }
    return {**payload, "manifest_sha256": digest(canonical_bytes(payload))}


def verify_manifest(root: Path, manifest: Mapping) -> list[str]:
    """Lista vacía = bytes y digest coinciden; no autenticación de autor."""
    errors = []
    try:
        payload = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
        if digest(canonical_bytes(payload)) != manifest["manifest_sha256"]:
            errors.append("manifest_digest_mismatch")
        if digest(canonical_bytes(manifest["config"])) != manifest["config_sha256"]:
            errors.append("config_digest_mismatch")
        for group in ("code", "data"):
            expected = manifest[group]
            actual = file_records(root, [record["path"] for record in expected])
            if actual != expected:
                errors.append(f"{group}_files_mismatch")
    except (KeyError, TypeError, ValueError, OSError) as exc:
        errors.append(f"invalid_manifest_or_files:{type(exc).__name__}")
    return errors


def write_manifest(path: Path, manifest: Mapping) -> None:
    # Creación exclusiva: no reemplaza una congelación anterior silenciosamente.
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(manifest, handle, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        handle.write("\n")
