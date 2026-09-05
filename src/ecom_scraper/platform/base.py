"""Platform adapter abstraction."""

from abc import ABC, abstractmethod

from ecom_scraper.models.product import Product
from ecom_scraper.models.shop import Shop
from ecom_scraper.models.sku import ProductSKU
from ecom_scraper.request.request import Request
from ecom_scraper.request.response import Response
from ecom_scraper.spider.base import Spider
from ecom_scraper.validator.product import validate_product


class PlatformAdapter(ABC):
    """Parses platform-specific responses into canonical models."""

    name: str = "platform"

    def product_requests(self, product_urls: list[str]) -> list[Request]:
        """Build requests for the given product URLs."""
        return [Request(url=url) for url in product_urls]

    @abstractmethod
    def parse_product(self, response: Response) -> Product:
        """Parse a response into a canonical product (without shop/skus)."""

    @abstractmethod
    def parse_shop(self, response: Response) -> Shop:
        """Parse a response into a canonical shop."""

    @abstractmethod
    def parse_skus(self, response: Response) -> list[ProductSKU]:
        """Parse a response into canonical SKUs."""


class PlatformSpider(Spider):
    """A spider that parses product pages via a platform adapter."""

    def __init__(self, adapter: PlatformAdapter, product_urls: list[str]) -> None:
        self._adapter = adapter
        self._product_urls = product_urls

    def start_requests(self) -> list[Request]:
        """Return product requests built by the adapter."""
        return self._adapter.product_requests(self._product_urls)

    def parse(self, response: Response) -> Product | None:
        """Parse a response into a validated canonical product."""
        product = self._adapter.parse_product(response)
        product = product.model_copy(
            update={
                "shop": self._adapter.parse_shop(response),
                "skus": self._adapter.parse_skus(response),
            }
        )
        validate_product(product)
        return product
