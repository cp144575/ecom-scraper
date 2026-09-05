from decimal import Decimal

import pytest
from pydantic import ValidationError

from ecom_scraper.models.product import Product


def test_product_accepts_valid_data() -> None:
    product = Product(
        platform="books",
        platform_product_id="a-light-in-the-attic_1000",
        title="A Light in the Attic",
        url="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        price=Decimal("51.77"),
        currency="GBP",
    )
    assert product.price == Decimal("51.77")
    assert product.currency == "GBP"


def test_product_defaults_currency_to_cny() -> None:
    product = Product(
        platform="p",
        platform_product_id="1",
        title="T",
        url="https://example.com",
    )
    assert product.currency == "CNY"
    assert product.price is None


def test_product_rejects_invalid_price() -> None:
    with pytest.raises(ValidationError):
        Product(
            platform="p",
            platform_product_id="1",
            title="T",
            url="https://example.com",
            price="not-a-decimal",
        )
