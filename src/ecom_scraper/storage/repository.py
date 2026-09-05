"""Async repository for persisting canonical products."""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ecom_scraper.models.product import Product
from ecom_scraper.storage.models import ProductRow


class AsyncProductRepository:
    """Persists and reads products through an async SQLAlchemy session."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def save(self, product: Product) -> None:
        """Insert a product, or update it when the platform id already exists."""
        async with self._session_factory() as session:
            row = await session.scalar(
                select(ProductRow).where(
                    ProductRow.platform == product.platform,
                    ProductRow.platform_product_id == product.platform_product_id,
                )
            )
            if row is None:
                session.add(
                    ProductRow(
                        platform=product.platform,
                        platform_product_id=product.platform_product_id,
                        title=product.title,
                        url=product.url,
                        price=product.price,
                        currency=product.currency,
                        captured_at=datetime.now(UTC),
                    )
                )
            else:
                row.title = product.title
                row.url = product.url
                row.price = product.price
                row.currency = product.currency
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
            return self._to_domain(row) if row is not None else None

    async def list_all(self) -> list[Product]:
        """Return every persisted product."""
        async with self._session_factory() as session:
            rows = await session.scalars(select(ProductRow))
            return [self._to_domain(row) for row in rows]

    @staticmethod
    def _to_domain(row: ProductRow) -> Product:
        return Product(
            platform=row.platform,
            platform_product_id=row.platform_product_id,
            title=row.title,
            url=row.url,
            price=row.price,
            currency=row.currency,
        )
