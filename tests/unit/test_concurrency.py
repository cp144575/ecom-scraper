import asyncio

from ecom_scraper.concurrency.controller import ConcurrencyController


async def test_global_limit_is_enforced() -> None:
    controller = ConcurrencyController(global_limit=2)
    active = 0
    peak = 0

    async def work() -> None:
        nonlocal active, peak
        async with controller.acquire("https://example.com/1"):
            active += 1
            peak = max(peak, active)
            await asyncio.sleep(0.01)
            active -= 1

    await asyncio.gather(*[work() for _ in range(10)])
    assert peak == 2


async def test_domain_limit_is_enforced() -> None:
    controller = ConcurrencyController(global_limit=10, default_domain_limit=2)
    active = 0
    peak = 0

    async def work() -> None:
        nonlocal active, peak
        async with controller.acquire("https://example.com/page"):
            active += 1
            peak = max(peak, active)
            await asyncio.sleep(0.01)
            active -= 1

    await asyncio.gather(*[work() for _ in range(10)])
    assert peak == 2
