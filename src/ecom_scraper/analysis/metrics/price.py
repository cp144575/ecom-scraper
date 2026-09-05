"""Price metric functions."""

from decimal import Decimal

from ecom_scraper.models.snapshot import PriceSnapshot


def price_metrics(snapshots: list[PriceSnapshot]) -> dict[str, Decimal | int]:
    """Return min, max, average, and count over price snapshots."""
    prices = [snapshot.price for snapshot in snapshots]
    if not prices:
        return {"count": 0}
    total = sum(prices, Decimal("0"))
    return {
        "count": len(prices),
        "min": min(prices),
        "max": max(prices),
        "avg": total / Decimal(len(prices)),
    }


def price_change_rate(snapshots: list[PriceSnapshot]) -> Decimal | None:
    """Return the change rate between the first and last snapshot."""
    if len(snapshots) < 2:
        return None
    first = snapshots[0].price
    last = snapshots[-1].price
    if first == 0:
        return Decimal("0")
    return (last - first) / first
