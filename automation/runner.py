from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .site_adapter import MockMetadataSite


def apply_and_verify(site: MockMetadataSite, changes: dict[str, Any]) -> dict[str, Any]:
    before = asdict(site.read())

    effective_changes = {
        key: value for key, value in changes.items()
        if key in before and str(before[key]) != str(value)
    }

    if not effective_changes:
        return {"status": "NO_CHANGE", "before": before, "after": before, "changes": {}}

    site.write(effective_changes)
    site.save()

    # Demo page writes values to window.savedRecord. A real adapter should
    # close/re-open or re-query the server-backed detail page here.
    saved = site.saved_payload()
    after = asdict(site.read())

    mismatches = {
        key: {"expected": str(value), "actual": str(saved.get(key, ""))}
        for key, value in effective_changes.items()
        if str(saved.get(key, "")) != str(value)
    }

    return {
        "status": "VERIFIED" if not mismatches else "UNKNOWN_AFTER_WRITE",
        "before": before,
        "after": after,
        "changes": effective_changes,
        "mismatches": mismatches,
    }
