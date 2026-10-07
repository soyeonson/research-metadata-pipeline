from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from playwright.sync_api import Page


@dataclass
class ArticleState:
    paper_id: str
    title: str
    oa: str
    project_number: str


class MockMetadataSite:
    """Public demo adapter for a local HTML form.

    Real internal-system selectors should live in a private adapter, not here.
    """

    def __init__(self, page: Page):
        self.page = page

    def read(self) -> ArticleState:
        return ArticleState(
            paper_id=self.page.locator("#paper_id").input_value(),
            title=self.page.locator("#title").input_value(),
            oa=self.page.locator("#oa").input_value(),
            project_number=self.page.locator("#project_number").input_value(),
        )

    def write(self, changes: dict[str, Any]) -> None:
        selector_map = {
            "title": "#title",
            "oa": "#oa",
            "project_number": "#project_number",
        }
        for key, value in changes.items():
            selector = selector_map.get(key)
            if selector is not None:
                self.page.locator(selector).fill("" if value is None else str(value))

    def save(self) -> None:
        self.page.locator("#save").click()

    def saved_payload(self) -> dict[str, str]:
        return self.page.evaluate("window.savedRecord || {}")
