from decimal import Decimal

import pytest

from ecom_scraper.exceptions import ValidationError
from ecom_scraper.models.product import Product
from ecom_scraper.validator.product import validate_product


def _product(**overrides: object) -> Product:
    data = {
        "platform": "jd",
        "platform_product_id": "1",
        "title": "T",
        "url": "https://example.com",
        "price": Decimal("1.00"),
    }
    data.update(overrides)
    return Product(**data)


def test_valid_product_passes() -> None:
    validate_product(_product())


def test_missing_title_raises() -> None:
    with pytest.raises(ValidationError):
        validate_product(_product(title=""))


def test_negative_price_raises() -> None:
    with pytest.raises(ValidationError):
        validate_product(_product(price=Decimal("-1.00")))
