"""YAML/JSON loading without writes or implicit defaults."""

import json
from pathlib import Path
from typing import Any

import yaml


class DocumentLoadError(ValueError):
    """A document cannot be decoded into one mapping."""


def load_document(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    try:
        text = source.read_text(encoding="utf-8")
        data = json.loads(text) if source.suffix.lower() == ".json" else yaml.safe_load(text)
    except (OSError, UnicodeError, json.JSONDecodeError, yaml.YAMLError) as exc:
        raise DocumentLoadError(str(exc)) from exc
    if not isinstance(data, dict):
        raise DocumentLoadError("document root must be a mapping")
    return data
