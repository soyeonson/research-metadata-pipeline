from __future__ import annotations

from typing import Any, Protocol


class MetadataProvider(Protocol):
    """Interface for APIs that return bibliographic metadata."""

    def fetch_metadata(self, identifier: str) -> dict[str, Any]: ...


def allowlisted_metadata(raw: dict[str, Any]) -> dict[str, Any]:
    """Keep only fields the public sample explicitly needs.

    Avoid storing whole provider responses because they can contain fields with
    different licensing or retention conditions.
    """
    allowed = {
        "doi",
        "title",
        "journal",
        "authors",
        "published",
        "publisher",
    }
    return {key: raw.get(key) for key in allowed if key in raw}
