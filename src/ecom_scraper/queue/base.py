"""Queue abstraction for the crawl frontier."""

from typing import Protocol

from ecom_scraper.request.request import Request


class Queue(Protocol):
    """A FIFO request queue with deduplication."""

    async def put(self, request: Request) -> bool:
        """Enqueue a request, returning False when it is a duplicate."""
        ...

    async def get(self) -> Request:
        """Dequeue the next request."""
        ...
