"""Analytics API routes."""

from decimal import Decimal

from fastapi import APIRouter, Depends

from ecom_scraper.analysis.comparison.platform import average_price_by_platform
from ecom_scraper.analysis.metrics.inventory import inventory_metrics
from ecom_scraper.analysis.metrics.price import price_metrics
from ecom_scraper.api.dependencies import get_repository
from ecom_scraper.storage.repository import AsyncProductRepository

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/products")
async def product_count(
    repository: AsyncProductRepository | None = Depends(get_repository),
) -> dict[str, int]:
    if repository is None:
        return {"count": 0}
    return {"count": len(await repository.list_all())}


@router.get("/prices")
async def price_analytics(
    platform: str,
    product_id: str,
    repository: AsyncProductRepository | None = Depends(get_repository),
) -> dict[str, Decimal | int]:
    if repository is None:
        return {"count": 0}
    snapshots = await repository.list_price_snapshots(platform, product_id)
    return price_metrics(snapshots)


@router.get("/inventory")
async def inventory_analytics(
    platform: str,
    product_id: str,
    repository: AsyncProductRepository | None = Depends(get_repository),
) -> dict[str, int]:
    if repository is None:
        return {"count": 0}
    snapshots = await repository.list_inventory_snapshots(platform, product_id)
    return inventory_metrics(snapshots)


@router.get("/platforms")
async def platform_comparison(
    repository: AsyncProductRepository | None = Depends(get_repository),
) -> dict[str, str]:
    if repository is None:
        return {}
    products = await repository.list_all()
    return {name: str(value) for name, value in average_price_by_platform(products).items()}
