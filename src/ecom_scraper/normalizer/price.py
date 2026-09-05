"""Price normalization helpers."""

import re
from decimal import Decimal, InvalidOperation

_PRICE_PATTERN = re.compile(r"[^0-9.\-]")


def normalize_price(value: object) -> Decimal | None:
    """Normalize a price value into a Decimal, or None when empty."""
    if value is None:
        return None
    if isinstance(value, Decimal):
        return value
    text = str(value).strip()
    cleaned = _PRICE_PATTERN.sub("", text)
    if not cleaned:
        return None
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None
