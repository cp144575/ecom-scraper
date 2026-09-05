"""Product SKU canonical model."""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductSKU(BaseModel):
    """A single sellable variant of a product."""

    model_config = ConfigDict(frozen=True)

    sku_id: str
    attributes: dict[str, str] = Field(default_factory=dict)
    price: Decimal | None = None
    currency: str = "CNY"
    stock: int | None = None
