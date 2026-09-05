"""Platform comparison functions."""

from decimal import Decimal

from ecom_scraper.models.product import Product


def average_price_by_platform(products: list[Product]) -> dict[str, Decimal]:
    """Return the average price per platform."""
    totals: dict[str, list[Decimal]] = {}
    for product in products:
        if product.price is None:
            continue
        totals.setdefault(product.platform, []).append(product.price)
    return {
        platform: sum(prices, Decimal("0")) / Decimal(len(prices))
        for platform, prices in totals.items()
    }
