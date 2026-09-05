"""Canonical product validation."""

from ecom_scraper.exceptions import ValidationError
from ecom_scraper.models.product import Product


def validate_product(product: Product) -> None:
    """Raise ValidationError when a canonical product is invalid."""
    if not product.platform:
        raise ValidationError("platform is required")
    if not product.platform_product_id:
        raise ValidationError("platform_product_id is required")
    if not product.title:
        raise ValidationError("title is required")
    if product.price is not None and product.price < 0:
        raise ValidationError("price must be non-negative")
    for sku in product.skus:
        if not sku.sku_id:
            raise ValidationError("sku_id is required")
        if sku.stock is not None and sku.stock < 0:
            raise ValidationError("stock must be non-negative")
