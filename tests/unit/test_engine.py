from ecom_scraper.concurrency.controller import ConcurrencyController
from ecom_scraper.engine.engine import AsyncEngine
from ecom_scraper.models.product import Product
from ecom_scraper.pipeline.pipeline import Pipeline
from ecom_scraper.queue.memory import MemoryQueue
from ecom_scraper.rate_limit.local import DomainRateLimiter
from ecom_scraper.request.request import Request
from ecom_scraper.request.response import Response
from ecom_scraper.retry.policy import RetryPolicy
from ecom_scraper.spider.base import Spider
from ecom_scraper.storage.repository import AsyncProductRepository


class _StubFetcher:
    async def fetch(self, request: Request) -> Response:
        return Response(
            request=request,
            url=request.url,
            status_code=200,
            headers={},
            body=b"<html></html>",
        )


class _StubSpider(Spider):
    def __init__(self, total: int) -> None:
        self._total = total

    def start_requests(self) -> list[Request]:
        return [Request(url=f"https://example.com/{i}") for i in range(self._total)]

    def parse(self, response: Response) -> Product | None:
        return Product(
            platform="test",
            platform_product_id=response.url.split("/")[-1],
            title="Test product",
            url=response.url,
        )


def _make_engine(
    repository: AsyncProductRepository, *, queue_maxsize: int = 0, concurrency: int = 4
) -> AsyncEngine:
    return AsyncEngine(
        fetcher=_StubFetcher(),
        pipeline=Pipeline(repository),
        queue=MemoryQueue(maxsize=queue_maxsize),
        concurrency=ConcurrencyController(global_limit=concurrency),
        retry_policy=RetryPolicy(max_attempts=1),
        rate_limiter=DomainRateLimiter(default_rate=0),
    )


async def test_engine_runs_full_loop(repository: AsyncProductRepository) -> None:
    engine = _make_engine(repository)
    products = await engine.run(_StubSpider(2))
    assert sorted(product.platform_product_id for product in products) == ["0", "1"]
    assert len(await repository.list_all()) == 2


async def test_engine_with_bounded_queue_does_not_deadlock(
    repository: AsyncProductRepository,
) -> None:
    engine = _make_engine(repository, queue_maxsize=2, concurrency=2)
    products = await engine.run(_StubSpider(20))
    assert len(products) == 20
    assert len(await repository.list_all()) == 20
