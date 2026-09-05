"""Demo spider for books.toscrape.com product pages."""

from ecom_scraper.models.product import Product
from ecom_scraper.parser.product import ProductParser
from ecom_scraper.request.response import Response
from ecom_scraper.spider.base import Spider


class BooksSpider(Spider):
    """Scrapes a single books.toscrape.com product page."""

    name = "books"
    start_urls = [
        "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    ]

    def __init__(self) -> None:
        self._parser = ProductParser(
            platform="books",
            title_selector="h1",
            price_selector="p.price_color",
            currency="GBP",
            product_id_regex=r"/catalogue/([^/]+)/",
        )

    def parse(self, response: Response) -> Product | None:
        """Parse a books.toscrape.com product page."""
        return self._parser.parse(response)
