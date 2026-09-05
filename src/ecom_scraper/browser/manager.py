"""Playwright browser manager."""

from typing import Any

from ecom_scraper.browser.context import BrowserContextFactory
from ecom_scraper.browser.pool import BrowserPool


class BrowserManager:
    """Owns a Playwright instance and a bounded browser pool."""

    def __init__(
        self,
        *,
        headless: bool = True,
        pool_size: int = 2,
        context_factory: BrowserContextFactory | None = None,
    ) -> None:
        self._headless = headless
        self._pool_size = pool_size
        self._context_factory = context_factory or BrowserContextFactory()
        self._playwright: Any = None
        self._browser: Any = None
        self._pool: BrowserPool | None = None

    async def start(self) -> None:
        """Launch the browser and build the context pool."""
        from playwright.async_api import async_playwright

        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=self._headless)
        self._pool = BrowserPool(
            self._browser,
            self._context_factory,
            pool_size=self._pool_size,
        )

    async def stop(self) -> None:
        """Close the pool, browser, and Playwright instance."""
        if self._pool is not None:
            await self._pool.close()
        if self._browser is not None:
            await self._browser.close()
        if self._playwright is not None:
            await self._playwright.stop()

    async def fetch_html(self, url: str, *, timeout_ms: int = 30000) -> str:
        """Render a URL, raising RuntimeError when not started."""
        if self._pool is None:
            raise RuntimeError("BrowserManager is not started")
        return await self._pool.fetch_html(url, timeout_ms=timeout_ms)
