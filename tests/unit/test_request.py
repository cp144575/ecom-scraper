from ecom_scraper.request.request import Request
from ecom_scraper.request.response import Response


def test_request_generates_unique_ids() -> None:
    first = Request(url="https://example.com")
    second = Request(url="https://example.com")
    assert first.request_id != second.request_id


def test_request_defaults() -> None:
    request = Request(url="https://example.com")
    assert request.method == "GET"
    assert request.headers == {}
    assert request.meta == {}


def test_response_holds_request_and_body() -> None:
    request = Request(url="https://example.com")
    response = Response(
        request=request,
        url=request.url,
        status_code=200,
        headers={"content-type": "text/html"},
        body=b"<html></html>",
    )
    assert response.request is request
    assert response.status_code == 200
    assert response.body == b"<html></html>"
