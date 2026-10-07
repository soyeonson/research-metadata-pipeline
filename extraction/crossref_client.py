from __future__ import annotations

from typing import Any
from urllib.parse import quote

import requests


class CrossrefClient:
    """Small bibliographic-metadata example.

    The mapper intentionally ignores `abstract` and any unneeded response
    fields. This module demonstrates an allow-list approach rather than raw
    response persistence.
    """

    def __init__(self, user_agent: str = "research-metadata-pipeline/1.0"):
        self.base_url = "https://api.crossref.org"
        self.user_agent = user_agent

    def fetch_metadata(self, doi: str) -> dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/works/{quote(doi, safe='')}",
            headers={"User-Agent": self.user_agent},
            timeout=30,
        )
        response.raise_for_status()
        message = response.json()["message"]
        return self._map_message(message)

    @staticmethod
    def _map_message(message: dict[str, Any]) -> dict[str, Any]:
        title_values = message.get("title") or []
        container_values = message.get("container-title") or []

        authors = []
        for author in message.get("author") or []:
            given = (author.get("given") or "").strip()
            family = (author.get("family") or "").strip()
            name = " ".join(part for part in (given, family) if part)
            if name:
                authors.append(name)

        date_parts = ((message.get("published") or {}).get("date-parts") or [[]])[0]
        published = "-".join(str(part) for part in date_parts) if date_parts else None

        return {
            "doi": message.get("DOI"),
            "title": title_values[0] if title_values else None,
            "journal": container_values[0] if container_values else None,
            "authors": authors,
            "published": published,
            "publisher": message.get("publisher"),
        }
