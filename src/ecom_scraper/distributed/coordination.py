"""Worker heartbeat and registry."""

import time

from redis.asyncio import Redis


class WorkerHeartbeat:
    """Publishes liveness, status, and load for a worker."""

    def __init__(self, redis: Redis, *, worker_id: str, ttl: float = 15.0) -> None:
        self._redis = redis
        self._worker_id = worker_id
        self._ttl = ttl

    async def beat(self, *, status: str = "running", load: int = 0) -> None:
        """Write heartbeat, status, and load keys."""
        now = time.time()
        await self._redis.set(f"worker:{self._worker_id}:heartbeat", now, ex=int(self._ttl))
        await self._redis.set(f"worker:{self._worker_id}:status", status)
        await self._redis.set(f"worker:{self._worker_id}:load", load)
        await self._redis.set(f"worker:{self._worker_id}:last_seen", now)

    async def is_alive(self) -> bool:
        """Return True when the heartbeat key is present."""
        return bool(await self._redis.exists(f"worker:{self._worker_id}:heartbeat"))
