"""Load test that drives many URLs through the async engine with a stub fetcher."""

import asyncio
import sys
import time

from ecom_scraper.concurrency.controller import ConcurrencyController
from ecom_scraper.engine.engine import AsyncEngine
from ecom_scraper.models.product import Product
from ecom_scraper.queue.memory import MemoryQueue
from ecom_scraper.rate_limit.local import DomainRateLimiter
from ecom_scraper.request.request import Request
from ecom_scraper.request.response import Response
from ecom_scraper.retry.policy import RetryPolicy
from ecom_scraper.spider.base import Spider


class _NoopPipeline:
    async def process(self, product: Product) -> None:
        return None


class _LatencyFetcher:
    def __init__(self, latency: float = 0.001) -> None:
        self._latency = latency
        self.latencies: list[float] = []

    async def fetch(self, request: Request) -> Response:
        start = time.monotonic()
        await asyncio.sleep(self._latency)
        self.latencies.append(time.monotonic() - start)
        return Response(request=request, url=request.url, status_code=200, headers={}, body=b"")


class _BulkSpider(Spider):
    def __init__(self, total: int) -> None:
        self._total = total

    def start_requests(self) -> list[Request]:
        return [Request(url=f"https://example.com/item/{i}") for i in range(self._total)]

    def parse(self, response: Response) -> Product | None:
        return Product(
            platform="bench",
            platform_product_id=response.url.rsplit("/", 1)[-1],
            title="bench",
            url=response.url,
        )


def _percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    index = round((len(values) - 1) * p)
    return values[index]


async def run(total: int, concurrency: int) -> dict[str, float]:
    fetcher = _LatencyFetcher()
    engine = AsyncEngine(
        fetcher=fetcher,
        pipeline=_NoopPipeline(),
        queue=MemoryQueue(maxsize=concurrency * 2),
        concurrency=ConcurrencyController(global_limit=concurrency),
        retry_policy=RetryPolicy(max_attempts=1),
        rate_limiter=DomainRateLimiter(default_rate=0),
    )
    start = time.monotonic()
    products = await engine.run(_BulkSpider(total), worker_count=concurrency)
    elapsed = time.monotonic() - start
    latencies = sorted(fetcher.latencies)
    return {
        "total": float(total),
        "products": float(len(products)),
        "elapsed": elapsed,
        "throughput": total / elapsed if elapsed else 0.0,
        "p50": _percentile(latencies, 0.50),
        "p95": _percentile(latencies, 0.95),
        "max": latencies[-1] if latencies else 0.0,
    }


def main() -> None:
    total = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000
    concurrency = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    metrics = asyncio.run(run(total, concurrency))
    print(
        f"total={metrics['total']:.0f} products={metrics['products']:.0f} "
        f"elapsed={metrics['elapsed']:.2f}s throughput={metrics['throughput']:.1f}/s "
        f"p50={metrics['p50'] * 1000:.1f}ms p95={metrics['p95'] * 1000:.1f}ms "
        f"max={metrics['max'] * 1000:.1f}ms"
    )


if __name__ == "__main__":
    main()
