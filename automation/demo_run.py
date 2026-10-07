from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

from .browser import open_demo_page
from .runner import apply_and_verify
from .site_adapter import MockMetadataSite


def main() -> int:
    html = Path(__file__).parent / "demo_site" / "article_form.html"
    with sync_playwright() as playwright:
        browser, context, page = open_demo_page(playwright, html)
        try:
            site = MockMetadataSite(page)
            result = apply_and_verify(
                site,
                {
                    "oa": "Y",
                    "project_number": "PRJ-002",
                },
            )
            print(json.dumps(result, ensure_ascii=False, indent=2))
            input("\nPress Enter to close the demo browser...")
        finally:
            context.close()
            browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
