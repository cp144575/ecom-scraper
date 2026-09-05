"""Repository for persisting canonical products."""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from ecom_scraper.models.product import Product
from ecom_scraper.storage.models import ProductRow


class ProductRepository:
    """Persists and reads products through a SQLAlchemy session."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def save(self, product: Product) -> None:
        """Insert a product, or update it when the platform id already exists."""
        with self._session_factory() as session:
            row = session.scalar(
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
            session.commit()

    def get(self, platform: str, platform_product_id: str) -> Product | None:
        """Return a product by platform and platform id, or None."""
        with self._session_factory() as session:
            row = session.scalar(
                select(ProductRow).where(
                    ProductRow.platform == platform,
                    ProductRow.platform_product_id == platform_product_id,
                )
            )
            return self._to_domain(row) if row is not None else None

    def list_all(self) -> list[Product]:
        """Return every persisted product."""
        with self._session_factory() as session:
            rows = session.scalars(select(ProductRow)).all()
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
