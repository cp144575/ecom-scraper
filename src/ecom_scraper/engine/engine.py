"""Asynchronous crawl engine that orchestrates the full pipeline."""

import asyncio

from structlog.stdlib import BoundLogger

from ecom_scraper.concurrency.controller import ConcurrencyController
from ecom_scraper.fetcher.base import Fetcher
from ecom_scraper.models.product import Product
from ecom_scraper.observability.metrics import crawler_items_total, crawler_requests_total
from ecom_scraper.pipeline.pipeline import PipelineLike
from ecom_scraper.queue.base import Queue
from ecom_scraper.rate_limit.local import DomainRateLimiter
from ecom_scraper.retry.policy import RetryPolicy, fetch_with_retry
from ecom_scraper.spider.base import Spider


class AsyncEngine:
    """Runs spiders through fetch -> parse -> pipeline using async workers."""

    def __init__(
        self,
        *,
        fetcher: Fetcher,
        pipeline: PipelineLike,
        queue: Queue,
        concurrency: ConcurrencyController,
        retry_policy: RetryPolicy,
        rate_limiter: DomainRateLimiter,
        logger: BoundLogger | None = None,
    ) -> None:
        self._fetcher = fetcher
        self._pipeline = pipeline
        self._queue = queue
        self._concurrency = concurrency
        self._retry_policy = retry_policy
        self._rate_limiter = rate_limiter
        self._logger = logger
        self._pending = 0
        self._pending_changed = asyncio.Condition()

    async def run(self, spider: Spider, *, worker_count: int | None = None) -> list[Product]:
        """Run a spider and return every product that was persisted."""
        products: list[Product] = []
        workers_count = worker_count or self._concurrency.global_limit
        workers = [
            asyncio.create_task(self._worker(spider, products)) for _ in range(workers_count)
        ]
        try:
            await self._seed(spider)
            async with self._pending_changed:
                while self._pending > 0:
                    await self._pending_changed.wait()
        finally:
            for worker in workers:
                worker.cancel()
            await asyncio.gather(*workers, return_exceptions=True)

        if self._logger is not None:
            self._logger.info("crawl_finished", products=len(products))
        return products

    async def _seed(self, spider: Spider) -> None:
        for request in spider.start_requests():
            added = await self._queue.put(request)
            if added:
                async with self._pending_changed:
                    self._pending += 1

    async def _worker(self, spider: Spider, products: list[Product]) -> None:
        while True:
            request = await self._queue.get()
            try:
                async with self._concurrency.acquire(request.url):
                    await self._rate_limiter.acquire(request.url)
                    response = await fetch_with_retry(
                        self._retry_policy,
                        self._fetcher.fetch,
                        request,
                    )
                    product = spider.parse(response)
                    if product is not None:
                        crawler_requests_total.labels(status="success").inc()
                        crawler_items_total.inc()
                        await self._pipeline.process(product)
                        products.append(product)
                    else:
                        crawler_requests_total.labels(status="no_product").inc()
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                crawler_requests_total.labels(status="failed").inc()
                if self._logger is not None:
                    self._logger.error(
                        "request_failed",
                        url=request.url,
                        error_type=type(exc).__name__,
                    )
            finally:
                async with self._pending_changed:
                    self._pending -= 1
                    self._pending_changed.notify_all()
