from datetime import UTC, datetime
from decimal import Decimal

from ecom_scraper.analysis.comparison.platform import average_price_by_platform
from ecom_scraper.analysis.metrics.inventory import inventory_metrics
from ecom_scraper.analysis.metrics.price import price_change_rate, price_metrics
from ecom_scraper.models.product import Product
from ecom_scraper.models.snapshot import InventorySnapshot, PriceSnapshot


def _price_snapshot(price: str, captured_at: datetime) -> PriceSnapshot:
    return PriceSnapshot(
        platform="jd",
        platform_product_id="1",
        price=Decimal(price),
        captured_at=captured_at,
    )


def test_price_metrics() -> None:
    now = datetime.now(UTC)
    metrics = price_metrics([_price_snapshot("10.00", now), _price_snapshot("20.00", now)])
    assert metrics == {
        "count": 2,
        "min": Decimal("10.00"),
        "max": Decimal("20.00"),
        "avg": Decimal("15.00"),
    }


def test_price_change_rate() -> None:
    now = datetime.now(UTC)
    rate = price_change_rate([_price_snapshot("10.00", now), _price_snapshot("12.00", now)])
    assert rate == Decimal("0.2")


def test_inventory_metrics() -> None:
    now = datetime.now(UTC)
    snapshots = [
        InventorySnapshot(platform="jd", platform_product_id="1", stock=100, captured_at=now),
        InventorySnapshot(platform="jd", platform_product_id="1", stock=20, captured_at=now),
    ]
    assert inventory_metrics(snapshots) == {
        "count": 2,
        "min": 20,
        "max": 100,
        "latest": 20,
    }


def test_average_price_by_platform() -> None:
    products = [
        Product(platform="jd", platform_product_id="1", title="A", url="u", price=Decimal("10")),
        Product(platform="jd", platform_product_id="2", title="B", url="u", price=Decimal("20")),
        Product(
            platform="amazon", platform_product_id="3", title="C", url="u", price=Decimal("30")
        ),
    ]
    assert average_price_by_platform(products) == {
        "jd": Decimal("15"),
        "amazon": Decimal("30"),
    }
