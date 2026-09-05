"""Shop canonical model."""

from pydantic import BaseModel, ConfigDict


class Shop(BaseModel):
    """A seller or merchant on a platform."""

    model_config = ConfigDict(frozen=True)

    platform: str
    platform_shop_id: str
    name: str | None = None
    url: str | None = None
