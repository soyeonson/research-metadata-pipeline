from __future__ import annotations

import json
from pathlib import Path
from typing import Any


FORBIDDEN_SOURCE_KEYS = {
    "source_text",
    "source_content",
    "full_text",
    "fulltext",
    "abstract",
    "abstract_text",
    "acknowledgement",
    "acknowledgements",
    "acknowledgment",
    "acknowledgments",
    "acknowledgement_text",
    "evidence_text",
    "source_html",
    "source_xml",
    "raw_response",
    "raw_payload",
}


def _find_forbidden_keys(value: Any, path: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in FORBIDDEN_SOURCE_KEYS:
                found.append(child_path)
            found.extend(_find_forbidden_keys(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_find_forbidden_keys(child, f"{path}[{index}]"))
    return found


def save_derived_json(payload: dict[str, Any], path: Path) -> None:
    """Persist structured results while blocking common source-content fields."""
    forbidden = _find_forbidden_keys(payload)
    if forbidden:
        raise ValueError("Refusing to persist source-content fields: " + ", ".join(forbidden))

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
