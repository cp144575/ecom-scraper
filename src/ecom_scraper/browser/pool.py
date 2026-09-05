"""Bounded pool of browser contexts."""

import asyncio
from typing import Any

from ecom_scraper.browser.context import BrowserContextFactory


class BrowserPool:
    """A small pool of browser contexts, one concurrent page per context."""

    def __init__(
        self,
        browser: Any,
        factory: BrowserContextFactory,
        *,
        pool_size: int,
    ) -> None:
        self._browser = browser
        self._factory = factory
        self._semaphore = asyncio.Semaphore(pool_size)

    async def fetch_html(self, url: str, *, timeout_ms: int) -> str:
        """Render a URL and return its HTML, bounded by the pool size."""
        async with self._semaphore:
            context = await self._factory.create(self._browser)
            try:
                page = await context.new_page()
                try:
                    await page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
                    return await page.content()
                finally:
                    await page.close()
            finally:
                await context.close()

    async def close(self) -> None:
        """Release pool resources (contexts are closed per-use)."""
