"""add ecommerce domain tables

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-05
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("products", sa.Column("shop_platform_id", sa.String(length=255), nullable=True))
    op.add_column("products", sa.Column("category", sa.String(length=255), nullable=True))
    op.add_column("products", sa.Column("brand", sa.String(length=255), nullable=True))
    op.add_column("products", sa.Column("images", sa.JSON(), nullable=True))

    op.create_table(
        "shops",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("platform", sa.String(length=64), nullable=False),
        sa.Column("platform_shop_id", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=512), nullable=True),
        sa.Column("url", sa.String(length=2048), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("platform", "platform_shop_id", name="uq_shop_platform_id"),
    )

    op.create_table(
        "product_skus",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("platform", sa.String(length=64), nullable=False),
        sa.Column("platform_product_id", sa.String(length=255), nullable=False),
        sa.Column("sku_id", sa.String(length=255), nullable=False),
        sa.Column("attributes", sa.JSON(), nullable=True),
        sa.Column("price", sa.Numeric(12, 2), nullable=True),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("platform", "platform_product_id", "sku_id", name="uq_sku"),
    )

    op.create_table(
        "price_snapshots",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("platform", sa.String(length=64), nullable=False),
        sa.Column("platform_product_id", sa.String(length=255), nullable=False),
        sa.Column("price", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "inventory_snapshots",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("platform", sa.String(length=64), nullable=False),
        sa.Column("platform_product_id", sa.String(length=255), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=False),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("inventory_snapshots")
    op.drop_table("price_snapshots")
    op.drop_table("product_skus")
    op.drop_table("shops")
    op.drop_column("products", "images")
    op.drop_column("products", "brand")
    op.drop_column("products", "category")
    op.drop_column("products", "shop_platform_id")
