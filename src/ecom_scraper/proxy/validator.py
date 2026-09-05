"""Proxy validation."""

import aiohttp

from ecom_scraper.proxy.base import Proxy


async def validate_proxy(
    proxy: Proxy,
    *,
    test_url: str = "https://example.com",
    timeout: float = 5.0,
) -> bool:
    """Return True when a request through the proxy succeeds."""
    timeout_obj = aiohttp.ClientTimeout(total=timeout)
    try:
        async with (
            aiohttp.ClientSession() as session,
            session.get(test_url, proxy=proxy.url, timeout=timeout_obj) as response,
        ):
            return response.status < 500
    except aiohttp.ClientError:
        return False
