from decimal import Decimal

import pytest
from pydantic import ValidationError

from ecom_scraper.models.product import Product
from ecom_scraper.models.shop import Shop
from ecom_scraper.models.sku import ProductSKU


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
    assert product.skus == []
    assert product.images == []


def test_product_rejects_invalid_price() -> None:
    with pytest.raises(ValidationError):
        Product(
            platform="p",
            platform_product_id="1",
            title="T",
            url="https://example.com",
            price="not-a-decimal",
        )


def test_product_embeds_shop_and_skus() -> None:
    product = Product(
        platform="jd",
        platform_product_id="1",
        title="T",
        url="https://example.com",
        shop=Shop(platform="jd", platform_shop_id="S1", name="某店"),
        skus=[ProductSKU(sku_id="A", attributes={"颜色": "黑"}, price=Decimal("1.0"))],
        images=["https://example.com/1.jpg"],
        category="手机",
        brand="某品牌",
    )
    assert product.shop is not None
    assert product.shop.platform_shop_id == "S1"
    assert product.skus[0].attributes == {"颜色": "黑"}
