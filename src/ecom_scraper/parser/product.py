"""HTML product parser built on selectolax."""

import re
from decimal import Decimal, InvalidOperation

from selectolax.parser import HTMLParser

from ecom_scraper.exceptions import ParseError
from ecom_scraper.models.product import Product
from ecom_scraper.request.response import Response

_PRICE_PATTERN = re.compile(r"[^0-9.\-]")


class ProductParser:
    """Parses a product detail page into a Product using CSS selectors."""

    def __init__(
        self,
        *,
        platform: str,
        title_selector: str,
        price_selector: str,
        currency: str = "CNY",
        product_id_regex: str | None = None,
    ) -> None:
        self._platform = platform
        self._title_selector = title_selector
        self._price_selector = price_selector
        self._currency = currency
        self._product_id_regex = re.compile(product_id_regex) if product_id_regex else None

    def parse(self, response: Response) -> Product:
        """Extract a canonical product from an HTML response."""
        tree = HTMLParser(response.body.decode("utf-8", errors="replace"))

        title_node = tree.css_first(self._title_selector)
        if title_node is None:
            raise ParseError(f"Title not found with selector {self._title_selector!r}")

        price_node = tree.css_first(self._price_selector)
        if price_node is None:
            raise ParseError(f"Price not found with selector {self._price_selector!r}")

        return Product(
            platform=self._platform,
            platform_product_id=self._extract_product_id(response.url),
            title=title_node.text(strip=True),
            url=response.url,
            price=self._parse_price(price_node.text(strip=True)),
            currency=self._currency,
        )

    def _parse_price(self, raw: str) -> Decimal | None:
        cleaned = _PRICE_PATTERN.sub("", raw)
        if not cleaned:
            return None
        try:
            return Decimal(cleaned)
        except InvalidOperation as exc:
            raise ParseError(f"Invalid price {raw!r}") from exc

    def _extract_product_id(self, url: str) -> str:
        if self._product_id_regex is not None:
            match = self._product_id_regex.search(url)
            if match is not None:
                return match.group(1) or match.group(0)
        segment = url.rstrip("/").split("/")[-1]
        if "." in segment:
            segment = url.rstrip("/").split("/")[-2]
        return segment or url
