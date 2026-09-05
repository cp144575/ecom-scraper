"""Canonical product model shared across platforms."""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from ecom_scraper.models.shop import Shop
from ecom_scraper.models.sku import ProductSKU


class Product(BaseModel):
    """A normalized product after platform parsing."""

    model_config = ConfigDict(frozen=True)

    platform: str
    platform_product_id: str
    title: str
    url: str
    price: Decimal | None = None
    currency: str = "CNY"
    shop: Shop | None = None
    skus: list[ProductSKU] = Field(default_factory=list)
    images: list[str] = Field(default_factory=list)
    category: str | None = None
    brand: str | None = None
