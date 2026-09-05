from decimal import Decimal
from pathlib import Path

from ecom_scraper.parser.product import ProductParser
from ecom_scraper.request.request import Request
from ecom_scraper.request.response import Response

_FIXTURE = Path(__file__).parent.parent / "fixtures" / "html" / "product.html"


def _response() -> Response:
    body = _FIXTURE.read_bytes()
    request = Request(
        url="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    )
    return Response(request=request, url=request.url, status_code=200, headers={}, body=body)


def test_product_parser_extracts_fields() -> None:
    parser = ProductParser(
        platform="books",
        title_selector="h1",
        price_selector="p.price_color",
        currency="GBP",
        product_id_regex=r"/catalogue/([^/]+)/",
    )
    product = parser.parse(_response())
    assert product.platform == "books"
    assert product.platform_product_id == "a-light-in-the-attic_1000"
    assert product.title == "A Light in the Attic"
    assert product.price == Decimal("51.77")
    assert product.currency == "GBP"
