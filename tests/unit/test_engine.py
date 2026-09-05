from ecom_scraper.engine.engine import Engine
from ecom_scraper.models.product import Product
from ecom_scraper.pipeline.pipeline import Pipeline
from ecom_scraper.request.request import Request
from ecom_scraper.request.response import Response
from ecom_scraper.spider.base import Spider
from ecom_scraper.storage.repository import ProductRepository


class _StubFetcher:
    def fetch(self, request: Request) -> Response:
        return Response(
            request=request,
            url=request.url,
            status_code=200,
            headers={},
            body=b"<html></html>",
        )


class _StubSpider(Spider):
    def start_requests(self) -> list[Request]:
        return [Request(url="https://example.com/1"), Request(url="https://example.com/2")]

    def parse(self, response: Response) -> Product | None:
        return Product(
            platform="test",
            platform_product_id=response.url.split("/")[-1],
            title="Test product",
            url=response.url,
        )


def test_engine_runs_full_loop(repository: ProductRepository) -> None:
    engine = Engine(fetcher=_StubFetcher(), pipeline=Pipeline(repository))
    products = engine.run(_StubSpider())
    assert [product.platform_product_id for product in products] == ["1", "2"]
    assert len(repository.list_all()) == 2
