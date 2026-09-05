"""Multi-worker distributed load test."""

import asyncio
import sys
import time

from fakeredis import FakeAsyncRedis

from ecom_scraper.concurrency.controller import ConcurrencyController
from ecom_scraper.distributed.coordination import WorkerHeartbeat
from ecom_scraper.distributed.queue import LeasingRedisQueue
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

_JD_JSON = (
    b'{"sku_id":"1000","title":"t","price":"1.00",'
    b'"shop":{"shop_id":"s"},"skus":[{"sku_id":"a","stock":1}]}'
)


class _NoopPipeline:
    async def process(self, product: Product) -> None:
        return None


class _StubFetcher:
    async def fetch(self, request: Request) -> Response:
        await asyncio.sleep(0.0005)
        return Response(
            request=request, url=request.url, status_code=200, headers={}, body=_JD_JSON
        )


def _make_engine() -> AsyncEngine:
    return AsyncEngine(
        fetcher=_StubFetcher(),
        pipeline=_NoopPipeline(),
        queue=MemoryQueue(),
        concurrency=ConcurrencyController(global_limit=10),
        retry_policy=RetryPolicy(max_attempts=1),
        rate_limiter=DomainRateLimiter(default_rate=0),
    )


async def run(total: int, workers: int) -> dict[str, float]:
    redis = FakeAsyncRedis()
    queue = LeasingRedisQueue(redis)
    await DistributedScheduler(queue).seed(
        [Request(url=f"https://example.com/item/{i}") for i in range(total)]
    )
    worker_instances = [
        DistributedWorker(
            worker_id=f"w{i}",
            queue=queue,
            engine=_make_engine(),
            adapter=JdAdapter(),
            heartbeat=WorkerHeartbeat(redis, worker_id=f"w{i}"),
        )
        for i in range(workers)
    ]
    start = time.monotonic()
    await asyncio.gather(*[worker.run(exit_on_empty=True) for worker in worker_instances])
    elapsed = time.monotonic() - start
    leaked = len(await queue.recover())
    return {
        "total": float(total),
        "workers": float(workers),
        "elapsed": elapsed,
        "throughput": total / elapsed if elapsed else 0.0,
        "leaked": float(leaked),
    }


def main() -> None:
    total = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    metrics = asyncio.run(run(total, workers))
    print(
        f"total={metrics['total']:.0f} workers={metrics['workers']:.0f} "
        f"elapsed={metrics['elapsed']:.2f}s throughput={metrics['throughput']:.1f}/s "
        f"leaked={metrics['leaked']:.0f}"
    )


if __name__ == "__main__":
    main()
