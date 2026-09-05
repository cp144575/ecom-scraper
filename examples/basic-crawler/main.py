"""Run a minimal async crawl against books.toscrape.com."""

import asyncio

from ecom_scraper.concurrency.controller import ConcurrencyController
from ecom_scraper.config.settings import Settings
from ecom_scraper.engine.engine import AsyncEngine
from ecom_scraper.fetcher.aiohttp import AiohttpFetcher
from ecom_scraper.pipeline.pipeline import Pipeline
from ecom_scraper.queue.memory import MemoryQueue
from ecom_scraper.rate_limit.local import DomainRateLimiter
from ecom_scraper.retry.policy import RetryPolicy
from ecom_scraper.spider.books import BooksSpider
from ecom_scraper.storage.repository import AsyncProductRepository
from ecom_scraper.storage.session import (
    create_all_async,
    create_async_session_factory,
    make_async_engine,
)


async def main() -> None:
    settings = Settings()
    engine = make_async_engine(settings.database_url)
    await create_all_async(engine)
    repository = AsyncProductRepository(create_async_session_factory(engine))
    fetcher = AiohttpFetcher(timeout=settings.request_timeout)
    try:
        crawler = AsyncEngine(
            fetcher=fetcher,
            pipeline=Pipeline(repository),
            queue=MemoryQueue(maxsize=settings.queue_maxsize),
            concurrency=ConcurrencyController(
                global_limit=settings.concurrency_global,
                default_domain_limit=settings.concurrency_domain_default,
            ),
            retry_policy=RetryPolicy(
                max_attempts=settings.retry_max_attempts,
                backoff_base=settings.retry_backoff_base,
                jitter=settings.retry_jitter,
            ),
            rate_limiter=DomainRateLimiter(default_rate=settings.rate_limit_rps),
        )
        products = await crawler.run(BooksSpider())
        for product in products:
            print(
                f"{product.platform_product_id}: {product.title} "
                f"@ {product.price} {product.currency}"
            )
        print(f"Saved {len(products)} product(s) to {settings.database_url}")
    finally:
        await fetcher.close()
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
