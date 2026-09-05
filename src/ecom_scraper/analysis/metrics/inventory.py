"""Inventory metric functions."""

from ecom_scraper.models.snapshot import InventorySnapshot


def inventory_metrics(snapshots: list[InventorySnapshot]) -> dict[str, int]:
    """Return count, min, max, and latest stock over snapshots."""
    if not snapshots:
        return {"count": 0}
    stocks = [snapshot.stock for snapshot in snapshots]
    return {
        "count": len(stocks),
        "min": min(stocks),
        "max": max(stocks),
        "latest": stocks[-1],
    }
