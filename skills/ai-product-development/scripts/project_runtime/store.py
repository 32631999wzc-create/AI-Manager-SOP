"""Small YAML store with atomic single-file updates."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import tempfile
from typing import Any

import yaml


class StoreError(ValueError):
    """Persistent state cannot be read or written safely."""


def load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise StoreError(f"cannot read {path}: {exc}") from exc


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)


def atomic_write(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = dump_yaml(data)
    handle = None
    temporary = None
    try:
        handle = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", delete=False,
            dir=path.parent, prefix=f".{path.name}.", suffix=".tmp",
        )
        temporary = Path(handle.name)
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
        handle.close()
        handle = None
        os.replace(temporary, path)
    except OSError as exc:
        raise StoreError(f"cannot write {path}: {exc}") from exc
    finally:
        if handle is not None:
            handle.close()
        if temporary is not None and temporary.exists():
            temporary.unlink()


def sha256_document(data: Any) -> str:
    return hashlib.sha256(dump_yaml(data).encode("utf-8")).hexdigest()
