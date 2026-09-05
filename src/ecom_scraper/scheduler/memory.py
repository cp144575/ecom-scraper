"""In-memory FIFO scheduler with URL deduplication."""

from collections import deque

from ecom_scraper.request.request import Request


class MemoryScheduler:
    """A first-in-first-out scheduler that skips duplicate URLs."""

    def __init__(self) -> None:
        self._queue: deque[Request] = deque()
        self._seen: set[str] = set()

    def add(self, request: Request) -> None:
        """Enqueue a request unless its URL was already scheduled."""
        if request.url in self._seen:
            return
        self._seen.add(request.url)
        self._queue.append(request)

    def next(self) -> Request | None:
        """Pop the next request, or None when empty."""
        if not self._queue:
            return None
        return self._queue.popleft()

    def __len__(self) -> int:
        return len(self._queue)
