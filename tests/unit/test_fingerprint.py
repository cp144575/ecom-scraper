from ecom_scraper.request.fingerprint import request_fingerprint
from ecom_scraper.request.request import Request


def test_fingerprint_normalizes_url() -> None:
    first = Request(url="https://EXAMPLE.com/path?b=2&a=1#frag")
    second = Request(url="https://example.com/path?a=1&b=2")
    assert request_fingerprint(first) == request_fingerprint(second)


def test_fingerprint_differs_by_path() -> None:
    first = request_fingerprint(Request(url="https://example.com/a"))
    second = request_fingerprint(Request(url="https://example.com/b"))
    assert first != second
