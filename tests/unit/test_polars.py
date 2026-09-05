from decimal import Decimal

from ecom_scraper.analysis.reports.product import product_count_by_platform, product_report
from ecom_scraper.models.product import Product


def _products() -> list[Product]:
    return [
        Product(platform="jd", platform_product_id="1", title="A", url="u", price=Decimal("10")),
        Product(platform="jd", platform_product_id="2", title="B", url="u", price=Decimal("20")),
        Product(
            platform="amazon", platform_product_id="3", title="C", url="u", price=Decimal("30")
        ),
    ]


def test_product_report_has_rows() -> None:
    df = product_report(_products())
    assert df.height == 3
    assert set(df["platform"].to_list()) == {"jd", "amazon"}


def test_product_count_by_platform() -> None:
    assert product_count_by_platform(_products()) == {"jd": 2, "amazon": 1}
