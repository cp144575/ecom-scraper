"""Distributed deduplication backed by Redis."""

from redis.asyncio import Redis


class RedisDedup:
    """Tracks seen request fingerprints in a Redis set."""

    def __init__(self, redis: Redis, *, key: str = "ecom_scraper:seen") -> None:
        self._redis = redis
        self._key = key

    async def mark_seen(self, fingerprint: str) -> bool:
        """Return True when the fingerprint was newly added."""
        return bool(await self._redis.sadd(self._key, fingerprint))
