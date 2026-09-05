"""A worker that leases tasks and processes them through the engine."""

import asyncio

from ecom_scraper.distributed.coordination import WorkerHeartbeat
from ecom_scraper.distributed.queue import LeasingRedisQueue
from ecom_scraper.engine.engine import AsyncEngine
from ecom_scraper.platform.base import PlatformAdapter, PlatformSpider


class DistributedWorker:
    """Leases URLs from the shared queue and runs them through the engine."""

    def __init__(
        self,
        *,
        worker_id: str,
        queue: LeasingRedisQueue,
        engine: AsyncEngine,
        adapter: PlatformAdapter,
        heartbeat: WorkerHeartbeat,
        lease_seconds: float = 30.0,
    ) -> None:
        self._worker_id = worker_id
        self._queue = queue
        self._engine = engine
        self._adapter = adapter
        self._heartbeat = heartbeat
        self._lease_seconds = lease_seconds

    async def run(
        self,
        *,
        max_tasks: int | None = None,
        poll_interval: float = 0.1,
        exit_on_empty: bool = False,
    ) -> int:
        """Lease and process tasks until the limit is reached or the queue drains."""
        processed = 0
        while max_tasks is None or processed < max_tasks:
            await self._heartbeat.beat()
            url = await self._queue.lease(lease_seconds=self._lease_seconds)
            if url is None:
                if exit_on_empty:
                    break
                await asyncio.sleep(poll_interval)
                continue
            spider = PlatformSpider(self._adapter, [url])
            await self._engine.run(spider, worker_count=1)
            await self._queue.ack(url)
            processed += 1
            await self._heartbeat.beat(load=processed)
        return processed
