"""Product listing route."""

from fastapi import APIRouter, Depends

from ecom_scraper.api.dependencies import get_repository
from ecom_scraper.models.product import Product
from ecom_scraper.storage.repository import AsyncProductRepository

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
async def list_products(
    repository: AsyncProductRepository | None = Depends(get_repository),
) -> list[Product]:
    """Return every persisted product."""
    if repository is None:
        return []
    return await repository.list_all()
