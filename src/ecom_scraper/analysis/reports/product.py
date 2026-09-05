"""Polars-based product reports."""

import polars as pl

from ecom_scraper.models.product import Product


def product_report(products: list[Product]) -> pl.DataFrame:
    """Build a DataFrame from products for batch analysis."""
    return pl.DataFrame(
        [
            {
                "platform": product.platform,
                "platform_product_id": product.platform_product_id,
                "title": product.title,
                "price": float(product.price) if product.price is not None else None,
                "currency": product.currency,
                "brand": product.brand,
                "category": product.category,
            }
            for product in products
        ]
    )


def product_count_by_platform(products: list[Product]) -> dict[str, int]:
    """Return the number of products per platform."""
    df = product_report(products)
    if df.is_empty():
        return {}
    grouped = df.group_by("platform").agg(pl.len().alias("count"))
    return {row["platform"]: int(row["count"]) for row in grouped.to_dicts()}
