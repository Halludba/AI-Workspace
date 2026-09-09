from __future__ import annotations
import hashlib, json
from pathlib import Path
from typing import Any

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_NAME = 'pdf_system_config.json'
SCHEMA_NAME = 'pdf_system_schema.json'
GENERATED_NAME = 'generated_rules.py'
MANIFEST_NAME = 'pdf_system_manifest.json'
REPORT_NAME = 'recursive_convergence_report.txt'


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def safe_artifact_path(root: Path, rel: str) -> Path:
    p = (root / rel).resolve()
    try:
        p.relative_to(root)
    except ValueError as e:
        raise RuntimeError(f'BLOCK: artifact path escapes artifact_root: {rel}') from e
    return p
