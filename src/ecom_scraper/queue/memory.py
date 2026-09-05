"""In-memory bounded queue with deduplication."""

import asyncio

from ecom_scraper.request.fingerprint import request_fingerprint
from ecom_scraper.request.request import Request


class MemoryQueue:
    """An in-memory FIFO queue backed by asyncio.Queue."""

    def __init__(self, maxsize: int = 0) -> None:
        self._queue: asyncio.Queue[Request] = asyncio.Queue(maxsize=maxsize)
        self._seen: set[str] = set()

    async def put(self, request: Request) -> bool:
        """Enqueue a request, returning False when it is a duplicate."""
        fingerprint = request_fingerprint(request)
        if fingerprint in self._seen:
            return False
        self._seen.add(fingerprint)
        await self._queue.put(request)
        return True

    async def get(self) -> Request:
        """Dequeue the next request."""
        return await self._queue.get()

    def qsize(self) -> int:
        """Return the number of pending requests."""
        return self._queue.qsize()

    def empty(self) -> bool:
        """Return True when the queue has no pending requests."""
        return self._queue.empty()
