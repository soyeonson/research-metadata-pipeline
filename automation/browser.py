import os
from pathlib import Path
from playwright.sync_api import Playwright


def open_demo_page(playwright: Playwright, html: Path):
    channel = os.getenv("PLAYWRIGHT_BROWSER_CHANNEL")

    launch_kwargs = {"headless": False}

    if channel:
        launch_kwargs["channel"] = channel

    browser = playwright.chromium.launch(**launch_kwargs)

    context = browser.new_context()
    page = context.new_page()
    page.goto(html.resolve().as_uri())

    return browser, context, page