import pytest

from ecom_scraper.browser.manager import BrowserManager

pytestmark = pytest.mark.skip(
    reason="Playwright browsers are not installed; run `playwright install chromium` to enable"
)


async def test_browser_manager_renders_page() -> None:
    manager = BrowserManager(headless=True, pool_size=1)
    await manager.start()
    try:
        html = await manager.fetch_html(
            "data:text/html,<html><body>hello</body></html>", timeout_ms=5000
        )
        assert "hello" in html
    finally:
        await manager.stop()
