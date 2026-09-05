"""Reliable Redis queue with task leasing and recovery."""

import time

from redis.asyncio import Redis

from ecom_scraper.distributed.dedup import RedisDedup
from ecom_scraper.request.fingerprint import request_fingerprint
from ecom_scraper.request.request import Request


class LeasingRedisQueue:
    """A reliable FIFO queue that leases tasks and recovers expired leases."""

    def __init__(
        self,
        redis: Redis,
        *,
        queue_key: str = "ecom_scraper:queue",
        processing_key: str = "ecom_scraper:processing",
        lease_key: str = "ecom_scraper:leases",
        dedup: RedisDedup | None = None,
    ) -> None:
        self._redis = redis
        self._queue_key = queue_key
        self._processing_key = processing_key
        self._lease_key = lease_key
        self._dedup = dedup or RedisDedup(redis)

    async def put(self, request: Request) -> bool:
        """Enqueue a request, returning False when it is a duplicate."""
        fingerprint = request_fingerprint(request)
        if not await self._dedup.mark_seen(fingerprint):
            return False
        await self._redis.rpush(self._queue_key, request.url)
        return True

    async def lease(self, *, lease_seconds: float = 30.0) -> str | None:
        """Atomically lease the next URL, or None when the queue is empty."""
        item = await self._redis.lmove(self._queue_key, self._processing_key, "RIGHT", "LEFT")
        if item is None:
            return None
        url = item.decode("utf-8") if isinstance(item, bytes) else str(item)
        await self._set_expiry(url, lease_seconds)
        return url

    async def heartbeat(self, url: str, *, lease_seconds: float = 30.0) -> None:
        """Refresh the lease for a URL currently being processed."""
        await self._set_expiry(url, lease_seconds)

    async def ack(self, url: str) -> None:
        """Remove a processed URL from the processing list and leases."""
        await self._redis.lrem(self._processing_key, 1, url)
        await self._redis.hdel(self._lease_key, url)

    async def recover(self, *, now: float | None = None) -> list[str]:
        """Requeue URLs whose lease has expired."""
        now = now or time.time()
        entries = await self._redis.hgetall(self._lease_key)
        recovered: list[str] = []
        for raw_url, raw_expiry in entries.items():
            url = raw_url.decode("utf-8") if isinstance(raw_url, bytes) else str(raw_url)
            if float(raw_expiry) < now:
                await self._redis.lrem(self._processing_key, 1, url)
                await self._redis.rpush(self._queue_key, url)
                await self._redis.hdel(self._lease_key, url)
                recovered.append(url)
        return recovered

    async def _set_expiry(self, url: str, lease_seconds: float) -> None:
        await self._redis.hset(self._lease_key, url, time.time() + lease_seconds)
