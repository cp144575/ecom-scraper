"""Time-series snapshot models."""

from datetime import UTC, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PriceSnapshot(BaseModel):
    """A point-in-time observation of a product price."""

    model_config = ConfigDict(frozen=True)

    platform: str
    platform_product_id: str
    price: Decimal
    currency: str = "CNY"
    captured_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class InventorySnapshot(BaseModel):
    """A point-in-time observation of a product's total stock."""

    model_config = ConfigDict(frozen=True)

    platform: str
    platform_product_id: str
    stock: int
    captured_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
