from __future__ import annotations

import re
import unicodedata
from typing import Iterable

DASHES = dict.fromkeys(map(ord, "‐‑‒–—―−"), "-")


def clean_text(value: object) -> str:
    if value is None:
        return ""
    text = unicodedata.normalize("NFKC", str(value)).translate(DASHES)
    return re.sub(r"\s+", " ", text).strip()


def normalize_simple(value: object) -> str:
    return clean_text(value).casefold()


def normalize_oa(value: object) -> str | None:
    text = normalize_simple(value)
    if not text:
        return None
    if text in {"y", "yes", "true", "1", "open", "open access"}:
        return "Y"
    if text in {"n", "no", "false", "0", "closed", "not open"}:
        return "N"
    return clean_text(value).upper()


def normalize_project_number(value: object, strip_prefixes: Iterable[str] = ()) -> str:
    text = clean_text(value).upper()
    if not text:
        return ""

    for prefix in strip_prefixes:
        prefix_clean = re.escape(clean_text(prefix).upper())
        text = re.sub(rf"^{prefix_clean}(?:\s*[:#-]\s*|\s+)", "", text)

    text = re.sub(r"\s*-\s*", "-", text)
    text = re.sub(r"\s+", "", text)
    return text


def split_semicolon(value: object) -> list[str]:
    text = clean_text(value)
    if not text:
        return []
    return [clean_text(part) for part in text.split(";") if clean_text(part)]


def build_authority_map(rows: Iterable[tuple[object, object]]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for variant, canonical in rows:
        v = normalize_simple(variant)
        c = clean_text(canonical)
        if v and c:
            mapping[v] = c
    return mapping


def normalize_affiliation(value: object, authority_map: dict[str, str] | None = None) -> str:
    text = clean_text(value)
    if not text:
        return ""
    if authority_map:
        canonical = authority_map.get(normalize_simple(text))
        if canonical:
            return clean_text(canonical)
    return text
