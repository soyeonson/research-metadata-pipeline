from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


def validate_json(input_path: str | Path, schema_path: str | Path) -> list[str]:
    data = json.loads(Path(input_path).read_text(encoding="utf-8"))
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    messages: list[str] = []
    for error in errors:
        location = ".".join(str(p) for p in error.absolute_path) or "<root>"
        messages.append(f"{location}: {error.message}")
    return messages


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate extracted metadata JSON against a JSON schema.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--schema", required=True)
    args = parser.parse_args()

    errors = validate_json(args.input, args.schema)
    if errors:
        print("Schema validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Schema validation PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
