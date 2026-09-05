import asyncio
from collections.abc import AsyncIterator
from pathlib import Path

import pytest
from fakeredis import FakeAsyncRedis

from ecom_scraper.concurrency.controller import ConcurrencyController
from ecom_scraper.distributed.coordination import WorkerHeartbeat, WorkerRegistry
from ecom_scraper.distributed.dedup import RedisDedup
from ecom_scraper.distributed.queue import LeasingRedisQueue
from ecom_scraper.distributed.rate_limit import RedisRateLimiter
from ecom_scraper.distributed.scheduler import DistributedScheduler
from ecom_scraper.distributed.worker import DistributedWorker
from ecom_scraper.engine.engine import AsyncEngine
from ecom_scraper.models.product import Product
from ecom_scraper.platform.cn.jd import JdAdapter
from ecom_scraper.queue.memory import MemoryQueue
from ecom_scraper.rate_limit.local import DomainRateLimiter
from ecom_scraper.request.request import Request
from ecom_scraper.request.response import Response
from ecom_scraper.retry.policy import RetryPolicy

_FIXTURE = Path(__file__).parent.parent / "fixtures" / "json" / "jd_product.json"


@pytest.fixture()
async def redis() -> AsyncIterator[FakeAsyncRedis]:
    client = FakeAsyncRedis()
    yield client
    await client.flushall()


async def test_redis_dedup_marks_seen(redis: FakeAsyncRedis) -> None:
    dedup = RedisDedup(redis)
    assert await dedup.mark_seen("fp-1") is True
    assert await dedup.mark_seen("fp-1") is False


async def test_leasing_queue_lease_and_ack(redis: FakeAsyncRedis) -> None:
    queue = LeasingRedisQueue(redis)
    assert await queue.put(Request(url="https://example.com/1")) is True
    assert await queue.lease(lease_seconds=30) == "https://example.com/1"
    assert await queue.lease(lease_seconds=30) is None
    await queue.ack("https://example.com/1")
    assert await queue.recover() == []


async def test_leasing_queue_recovers_expired_lease(redis: FakeAsyncRedis) -> None:
    queue = LeasingRedisQueue(redis)
    await queue.put(Request(url="https://example.com/1"))
    assert await queue.lease(lease_seconds=0.01) == "https://example.com/1"
    await asyncio.sleep(0.05)
    assert await queue.recover() == ["https://example.com/1"]
    assert await queue.lease(lease_seconds=30) == "https://example.com/1"


async def test_redis_rate_limiter_blocks_over_rate(redis: FakeAsyncRedis) -> None:
    limiter = RedisRateLimiter(redis)
    await limiter.acquire("domain:example.com", rate=2, window=100)
    await limiter.acquire("domain:example.com", rate=2, window=100)
    third = asyncio.create_task(limiter.acquire("domain:example.com", rate=2, window=100))
    await asyncio.sleep(0.1)
    assert not third.done()
    third.cancel()


async def test_worker_heartbeat_tracks_liveness(redis: FakeAsyncRedis) -> None:
    heartbeat = WorkerHeartbeat(redis, worker_id="w1", ttl=15)
    assert await heartbeat.is_alive() is False
    await heartbeat.beat(status="running", load=3)
    assert await heartbeat.is_alive() is True


async def test_worker_registry_lists_workers(redis: FakeAsyncRedis) -> None:
    await WorkerHeartbeat(redis, worker_id="w1").beat()
    await WorkerHeartbeat(redis, worker_id="w2").beat()
    registry = WorkerRegistry(redis)
    assert await registry.list_workers() == ["w1", "w2"]
    info = await registry.get_worker("w1")
    assert info["status"] == "running"


class _NoopPipeline:
    async def process(self, product: Product) -> None:
        return None


class _FixtureFetcher:
    def __init__(self) -> None:
        self.body = _FIXTURE.read_bytes()

    async def fetch(self, request: Request) -> Response:
        return Response(
            request=request, url=request.url, status_code=200, headers={}, body=self.body
        )


def _make_engine() -> AsyncEngine:
    return AsyncEngine(
        fetcher=_FixtureFetcher(),
        pipeline=_NoopPipeline(),
        queue=MemoryQueue(),
        concurrency=ConcurrencyController(global_limit=2),
        retry_policy=RetryPolicy(max_attempts=1),
        rate_limiter=DomainRateLimiter(default_rate=0),
    )


async def test_distributed_worker_leases_and_acks(redis: FakeAsyncRedis) -> None:
    queue = LeasingRedisQueue(redis)
    scheduler = DistributedScheduler(queue)
    await scheduler.seed(
        [Request(url="https://example.com/1"), Request(url="https://example.com/2")]
    )
    worker = DistributedWorker(
        worker_id="w1",
        queue=queue,
        engine=_make_engine(),
        adapter=JdAdapter(),
        heartbeat=WorkerHeartbeat(redis, worker_id="w1"),
    )
    processed = await worker.run(max_tasks=2)
    assert processed == 2
    assert await queue.lease(lease_seconds=1) is None
