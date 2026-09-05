"""Local token-bucket rate limiting."""

import asyncio
import time
from urllib.parse import urlsplit


class TokenBucket:
    """A token bucket that limits the rate of acquisitions."""

    def __init__(self, *, rate: float, capacity: float | None = None) -> None:
        if rate <= 0:
            raise ValueError("rate must be positive")
        self._rate = rate
        self._capacity = capacity if capacity is not None else rate
        self._tokens = self._capacity
        self._updated = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Acquire one token, waiting until one is available."""
        async with self._lock:
            while True:
                now = time.monotonic()
                elapsed = now - self._updated
                self._tokens = min(self._capacity, self._tokens + elapsed * self._rate)
                self._updated = now
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return
                await asyncio.sleep((1.0 - self._tokens) / self._rate)


class DomainRateLimiter:
    """Per-domain token buckets sharing a default rate."""

    def __init__(self, *, default_rate: float, rates: dict[str, float] | None = None) -> None:
        self._default_rate = default_rate
        self._rates = rates or {}
        self._buckets: dict[str, TokenBucket] = {}

    async def acquire(self, url: str) -> None:
        """Acquire a token for the URL's domain, or return immediately when unlimited."""
        domain = (urlsplit(url).netloc or "default").lower()
        rate = self._rates.get(domain, self._default_rate)
        if rate <= 0:
            return
        bucket = self._buckets.get(domain)
        if bucket is None:
            bucket = self._buckets[domain] = TokenBucket(rate=rate)
        await bucket.acquire()
