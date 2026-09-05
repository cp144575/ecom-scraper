"""Periodic recovery of expired task leases."""

import asyncio

from ecom_scraper.distributed.queue import LeasingRedisQueue


async def recover_loop(queue: LeasingRedisQueue, *, interval: float = 5.0) -> None:
    """Recover expired leases forever, sleeping between passes."""
    while True:
        await queue.recover()
        await asyncio.sleep(interval)
