"""SQLAlchemy ORM models."""

from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import JSON, DateTime, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def _utc_now() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


class ProductRow(Base):
    """Persisted canonical product."""

    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint("platform", "platform_product_id", name="uq_product_platform_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    platform: Mapped[str] = mapped_column(String(64))
    platform_product_id: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(512))
    url: Mapped[str] = mapped_column(String(2048))
    price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(8))
    shop_platform_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    category: Mapped[str | None] = mapped_column(String(255), nullable=True)
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True)
    images: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utc_now)


class ShopRow(Base):
    """Persisted canonical shop."""

    __tablename__ = "shops"
    __table_args__ = (UniqueConstraint("platform", "platform_shop_id", name="uq_shop_platform_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    platform: Mapped[str] = mapped_column(String(64))
    platform_shop_id: Mapped[str] = mapped_column(String(255))
    name: Mapped[str | None] = mapped_column(String(512), nullable=True)
    url: Mapped[str | None] = mapped_column(String(2048), nullable=True)


class ProductSkuRow(Base):
    """Persisted product SKU."""

    __tablename__ = "product_skus"
    __table_args__ = (UniqueConstraint("platform", "platform_product_id", "sku_id", name="uq_sku"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    platform: Mapped[str] = mapped_column(String(64))
    platform_product_id: Mapped[str] = mapped_column(String(255))
    sku_id: Mapped[str] = mapped_column(String(255))
    attributes: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)
    price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(8))
    stock: Mapped[int | None] = mapped_column(Integer, nullable=True)


class PriceSnapshotRow(Base):
    """Persisted price observation."""

    __tablename__ = "price_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    platform: Mapped[str] = mapped_column(String(64))
    platform_product_id: Mapped[str] = mapped_column(String(255))
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(8))
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utc_now)


class InventorySnapshotRow(Base):
    """Persisted inventory observation."""

    __tablename__ = "inventory_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    platform: Mapped[str] = mapped_column(String(64))
    platform_product_id: Mapped[str] = mapped_column(String(255))
    stock: Mapped[int] = mapped_column(Integer)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utc_now)
