"""Currency normalization helpers."""

_SYMBOLS = {"¥": "CNY", "￥": "CNY", "CN¥": "CNY", "£": "GBP", "€": "EUR", "$": "USD", "US$": "USD"}


def normalize_currency(value: object) -> str:
    """Normalize a currency symbol or code into an ISO 4217 code."""
    if value is None:
        return "CNY"
    code = str(value).strip().upper()
    if code in _SYMBOLS:
        return _SYMBOLS[code]
    if len(code) == 3 and code.isalpha():
        return code
    return "CNY"
