"""
Smoke test — validates that the whole pipeline works:
stack boots, frontend serves the SPA, Playwright can drive it.

Use this as a template. Real flows belong in their own test files
(e.g. test_text_blocks.py, test_login.py).
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_home_page_loads(base_url: str, page: Page) -> None:
    """The frontend root responds and has a <body>."""
    page.goto(base_url)
    expect(page.locator("body")).to_be_visible()


@pytest.mark.smoke
def test_api_proxy_is_reachable(base_url: str, page: Page) -> None:
    """The frontend's nginx proxies /api/ to the backend.
    We check it from inside the browser context so cookies, CORS and
    network rewrites behave like in real usage."""
    response = page.request.get(f"{base_url}/api/")
    # Whatever the API root returns (200, 404, redirect…) we want it to
    # NOT be a 502/504 — those mean the proxy can't reach the backend.
    assert response.status < 500, (
        f"API proxy unreachable: HTTP {response.status} — "
        "is the api container healthy?"
    )
