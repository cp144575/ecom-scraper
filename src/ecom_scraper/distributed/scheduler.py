"""Distributed scheduler that seeds the shared queue."""

from collections.abc import Iterable

from ecom_scraper.distributed.queue import LeasingRedisQueue
from ecom_scraper.request.request import Request


class DistributedScheduler:
    """Seeds the shared Redis queue."""

    def __init__(self, queue: LeasingRedisQueue) -> None:
        self._queue = queue

    async def seed(self, requests: Iterable[Request]) -> int:
        """Enqueue requests and return how many were newly added."""
        count = 0
        for request in requests:
            if await self._queue.put(request):
                count += 1
        return count
