from decimal import Decimal

from ecom_scraper.normalizer.currency import normalize_currency
from ecom_scraper.normalizer.price import normalize_price


def test_normalize_price_strips_symbol() -> None:
    assert normalize_price("¥3999.00") == Decimal("3999.00")
    assert normalize_price("$49.99") == Decimal("49.99")
    assert normalize_price("") is None
    assert normalize_price(None) is None


def test_normalize_currency() -> None:
    assert normalize_currency("¥") == "CNY"
    assert normalize_currency("$") == "USD"
    assert normalize_currency("GBP") == "GBP"
    assert normalize_currency(None) == "CNY"
