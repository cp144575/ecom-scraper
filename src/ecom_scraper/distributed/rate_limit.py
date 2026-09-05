"""Distributed rate limiting backed by Redis."""

import asyncio

from redis.asyncio import Redis


class RedisRateLimiter:
    """A fixed-window per-scope rate limiter shared across workers."""

    def __init__(self, redis: Redis, *, prefix: str = "ecom_scraper:rl") -> None:
        self._redis = redis
        self._prefix = prefix

    async def acquire(self, scope: str, *, rate: float, window: float = 1.0) -> None:
        """Wait until a request to the given scope is allowed."""
        if rate <= 0:
            return
        key = f"{self._prefix}:{scope}"
        while True:
            count = await self._redis.incr(key)
            if count == 1:
                await self._redis.expire(key, max(1, int(window)))
            if count <= rate:
                return
            await asyncio.sleep(0.05)
