"""Redis-backed queue with deduplication."""

from redis.asyncio import Redis

from ecom_scraper.request.fingerprint import request_fingerprint
from ecom_scraper.request.request import Request


class RedisQueue:
    """A Redis-backed FIFO queue; stores URLs and deduplicates by fingerprint."""

    def __init__(
        self,
        redis: Redis,
        *,
        key: str = "ecom_scraper:queue",
        seen_key: str = "ecom_scraper:seen",
    ) -> None:
        self._redis = redis
        self._key = key
        self._seen_key = seen_key

    async def put(self, request: Request) -> bool:
        """Enqueue a request, returning False when it is a duplicate."""
        fingerprint = request_fingerprint(request)
        added = await self._redis.sadd(self._seen_key, fingerprint)
        if not added:
            return False
        await self._redis.rpush(self._key, request.url)
        return True

    async def get(self) -> Request:
        """Dequeue the next request, blocking until one is available."""
        item = await self._redis.blpop(self._key)
        while item is None:
            item = await self._redis.blpop(self._key)
        value = item[1]
        url = value.decode("utf-8") if isinstance(value, bytes) else str(value)
        return Request(url=url)
