from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
from typing import Any

from storage.result_store import save_derived_json

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _line_value(text: str, prefix: str) -> str | None:
    for line in text.splitlines():
        if line.startswith(prefix):
            value = line[len(prefix):].strip()
            return value or None
    return None


def extract_from_synthetic_text(source_text: str, paper_id: str, source_hash: str) -> dict[str, Any]:
    """Extract a tiny public-demo metadata set from a synthetic fixture.

    This is deliberately not a general scholarly full-text parser. Its purpose
    is to demonstrate the persistence boundary: source text goes in, derived
    fields come out, and the returned object contains no source-content field.
    """
    title = _line_value(source_text, "Title:")
    journal = _line_value(source_text, "Journal:")

    oa = "Y" if "marked as Open Access for testing purposes only" in source_text else None
    project_numbers = sorted(set(re.findall(r"\bDEMO-\d{4}-\d{3}\b", source_text)))

    authors: list[dict[str, Any]] = []
    author_pattern = re.compile(
    r"^(?P<name>[^\n—]+)\s+—\s+(?P<affiliation>[^\n—]+)\s+—\s+(?P<role>First author|Corresponding author|Coauthor)$",
    re.MULTILINE,
    )
    
    role_map = {
        "First author": "first",
        "Corresponding author": "corresponding",
        "Coauthor": "coauthor",
    }
    for match in author_pattern.finditer(source_text):
        authors.append(
            {
                "name": match.group("name").strip(),
                "role": role_map[match.group("role")],
                "affiliations": [match.group("affiliation").strip()],
            }
        )

    return {
        "paper_id": paper_id,
        "title": title,
        "journal": journal,
        "open_access": oa,
        "project_numbers": project_numbers,
        "authors": authors,
        "provenance": {
            "source_hash": source_hash,
            "source_type": "synthetic_text",
            "source_locator": {
                "section": "synthetic fixture",
                "page": None,
            },
            "persistence_policy": "derived_metadata_only",
        },
    }


def process_file(path: Path, paper_id: str) -> dict[str, Any]:
    raw_bytes = path.read_bytes()
    source_hash = sha256_bytes(raw_bytes)

    # Source content exists only within this processing call. It is not placed
    # in the returned payload or written by this module.
    source_text = raw_bytes.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    
    try:
        paper = extract_from_synthetic_text(source_text, paper_id, source_hash)
        return {"papers": [paper]}
    finally:
        source_text = ""
        raw_bytes = b""


def main() -> None:
    parser = argparse.ArgumentParser(description="Process a synthetic document without persisting source text.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--paper-id", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = process_file(args.input, args.paper_id)
    save_derived_json(payload, args.output)
    print(f"Wrote derived metadata only: {args.output}")


if __name__ == "__main__":
    main()
