"""Canonical product model shared across platforms."""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    """A normalized product after platform parsing."""

    model_config = ConfigDict(frozen=True)

    platform: str
    platform_product_id: str
    title: str
    url: str
    price: Decimal | None = None
    currency: str = "CNY"
