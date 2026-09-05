import httpx
import pytest

from ecom_scraper.exceptions import FetchError
from ecom_scraper.fetcher.http import HttpxFetcher
from ecom_scraper.request.request import Request


def test_fetcher_returns_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="<html></html>")

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport) as client:
        fetcher = HttpxFetcher(client=client)
        response = fetcher.fetch(Request(url="https://example.com"))
    assert response.status_code == 200
    assert response.body == b"<html></html>"


def test_fetcher_wraps_network_error_as_fetch_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom", request=request)

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport) as client:
        fetcher = HttpxFetcher(client=client)
        with pytest.raises(FetchError):
            fetcher.fetch(Request(url="https://example.com"))
