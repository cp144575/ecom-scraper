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


class WorkerRegistry:
    """Discovers workers and their status from Redis."""

    def __init__(self, redis: Redis, *, key_prefix: str = "worker:") -> None:
        self._redis = redis
        self._key_prefix = key_prefix

    async def list_workers(self) -> list[str]:
        """Return the ids of workers that have published a status."""
        keys = await self._redis.keys(f"{self._key_prefix}*:status")
        worker_ids: set[str] = set()
        for key in keys:
            text = key.decode("utf-8") if isinstance(key, bytes) else str(key)
            parts = text.split(":")
            if len(parts) >= 2:
                worker_ids.add(parts[1])
        return sorted(worker_ids)

    async def get_worker(self, worker_id: str) -> dict[str, str]:
        """Return the status and load for a worker."""
        status = await self._redis.get(f"{self._key_prefix}{worker_id}:status")
        load = await self._redis.get(f"{self._key_prefix}{worker_id}:load")
        return {
            "worker_id": worker_id,
            "status": _decode(status) or "unknown",
            "load": _decode(load) or "0",
        }


def _decode(value: bytes | str | None) -> str | None:
    if value is None:
        return None
    return value.decode("utf-8") if isinstance(value, bytes) else value
