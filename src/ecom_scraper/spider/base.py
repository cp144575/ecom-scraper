"""Spider base class."""

from ecom_scraper.models.product import Product
from ecom_scraper.request.request import Request
from ecom_scraper.request.response import Response


class Spider:
    """Produces requests and turns responses into products."""

    name: str = "spider"
    start_urls: list[str] = []

    def start_requests(self) -> list[Request]:
        """Return the initial requests to schedule."""
        return [Request(url=url) for url in self.start_urls]

    def parse(self, response: Response) -> Product | None:
        """Parse a response into a product, or None to skip."""
        raise NotImplementedError
