"""Async repository for persisting canonical products and snapshots."""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ecom_scraper.models.product import Product
from ecom_scraper.models.shop import Shop
from ecom_scraper.models.sku import ProductSKU
from ecom_scraper.models.snapshot import InventorySnapshot, PriceSnapshot
from ecom_scraper.storage.models import (
    InventorySnapshotRow,
    PriceSnapshotRow,
    ProductRow,
    ProductSkuRow,
    ShopRow,
)


class AsyncProductRepository:
    """Persists and reads products, shops, SKUs, and snapshots."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def save(self, product: Product) -> None:
        """Persist a product with its shop, SKUs, and price/inventory snapshots."""
        now = datetime.now(UTC)
        async with self._session_factory() as session:
            if product.shop is not None:
                await self._upsert_shop(session, product.shop)
            await self._upsert_product(session, product)
            await self._upsert_skus(session, product)
            if product.price is not None:
                session.add(
                    PriceSnapshotRow(
                        platform=product.platform,
                        platform_product_id=product.platform_product_id,
                        price=product.price,
                        currency=product.currency,
                        captured_at=now,
                    )
                )
            stocks = [sku.stock for sku in product.skus if sku.stock is not None]
            if stocks:
                session.add(
                    InventorySnapshotRow(
                        platform=product.platform,
                        platform_product_id=product.platform_product_id,
                        stock=sum(stocks),
                        captured_at=now,
                    )
                )
            await session.commit()

    async def get(self, platform: str, platform_product_id: str) -> Product | None:
        """Return a product by platform and platform id, or None."""
        async with self._session_factory() as session:
            row = await session.scalar(
                select(ProductRow).where(
                    ProductRow.platform == platform,
                    ProductRow.platform_product_id == platform_product_id,
                )
            )
            return self._to_product(row) if row is not None else None

    async def list_all(self) -> list[Product]:
        """Return every persisted product."""
        async with self._session_factory() as session:
            rows = await session.scalars(select(ProductRow))
            return [self._to_product(row) for row in rows]

    async def list_price_snapshots(
        self, platform: str, platform_product_id: str
    ) -> list[PriceSnapshot]:
        """Return price observations for a product, oldest first."""
        async with self._session_factory() as session:
            rows = await session.scalars(
                select(PriceSnapshotRow)
                .where(
                    PriceSnapshotRow.platform == platform,
                    PriceSnapshotRow.platform_product_id == platform_product_id,
                )
                .order_by(PriceSnapshotRow.captured_at)
            )
            return [
                PriceSnapshot(
                    platform=row.platform,
                    platform_product_id=row.platform_product_id,
                    price=row.price,
                    currency=row.currency,
                    captured_at=row.captured_at,
                )
                for row in rows
            ]

    async def list_inventory_snapshots(
        self, platform: str, platform_product_id: str
    ) -> list[InventorySnapshot]:
        """Return inventory observations for a product, oldest first."""
        async with self._session_factory() as session:
            rows = await session.scalars(
                select(InventorySnapshotRow)
                .where(
                    InventorySnapshotRow.platform == platform,
                    InventorySnapshotRow.platform_product_id == platform_product_id,
                )
                .order_by(InventorySnapshotRow.captured_at)
            )
            return [
                InventorySnapshot(
                    platform=row.platform,
                    platform_product_id=row.platform_product_id,
                    stock=row.stock,
                    captured_at=row.captured_at,
                )
                for row in rows
            ]

    async def _upsert_shop(self, session: AsyncSession, shop: Shop) -> None:
        row = await session.scalar(
            select(ShopRow).where(
                ShopRow.platform == shop.platform,
                ShopRow.platform_shop_id == shop.platform_shop_id,
            )
        )
        if row is None:
            session.add(
                ShopRow(
                    platform=shop.platform,
                    platform_shop_id=shop.platform_shop_id,
                    name=shop.name,
                    url=shop.url,
                )
            )
        else:
            row.name = shop.name
            row.url = shop.url

    async def _upsert_product(self, session: AsyncSession, product: Product) -> None:
        row = await session.scalar(
            select(ProductRow).where(
                ProductRow.platform == product.platform,
                ProductRow.platform_product_id == product.platform_product_id,
            )
        )
        shop_platform_id = product.shop.platform_shop_id if product.shop is not None else None
        if row is None:
            session.add(
                ProductRow(
                    platform=product.platform,
                    platform_product_id=product.platform_product_id,
                    title=product.title,
                    url=product.url,
                    price=product.price,
                    currency=product.currency,
                    shop_platform_id=shop_platform_id,
                    category=product.category,
                    brand=product.brand,
                    images=product.images,
                    captured_at=datetime.now(UTC),
                )
            )
        else:
            row.title = product.title
            row.url = product.url
            row.price = product.price
            row.currency = product.currency
            row.shop_platform_id = shop_platform_id
            row.category = product.category
            row.brand = product.brand
            row.images = product.images

    async def _upsert_skus(self, session: AsyncSession, product: Product) -> None:
        for sku in product.skus:
            await self._upsert_sku(session, product, sku)

    async def _upsert_sku(self, session: AsyncSession, product: Product, sku: ProductSKU) -> None:
        row = await session.scalar(
            select(ProductSkuRow).where(
                ProductSkuRow.platform == product.platform,
                ProductSkuRow.platform_product_id == product.platform_product_id,
                ProductSkuRow.sku_id == sku.sku_id,
            )
        )
        if row is None:
            session.add(
                ProductSkuRow(
                    platform=product.platform,
                    platform_product_id=product.platform_product_id,
                    sku_id=sku.sku_id,
                    attributes=sku.attributes,
                    price=sku.price,
                    currency=sku.currency,
                    stock=sku.stock,
                )
            )
        else:
            row.attributes = sku.attributes
            row.price = sku.price
            row.currency = sku.currency
            row.stock = sku.stock

    @staticmethod
    def _to_product(row: ProductRow) -> Product:
        return Product(
            platform=row.platform,
            platform_product_id=row.platform_product_id,
            title=row.title,
            url=row.url,
            price=row.price,
            currency=row.currency,
            category=row.category,
            brand=row.brand,
            images=list(row.images or []),
        )
