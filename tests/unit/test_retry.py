import pytest

from ecom_scraper.exceptions import FetchError
from ecom_scraper.request.request import Request
from ecom_scraper.request.response import Response
from ecom_scraper.retry.policy import RetryPolicy, fetch_with_retry


async def _noop_sleep(_: float) -> None:
    return None


def _response(status: int = 200) -> Response:
    request = Request(url="https://example.com")
    return Response(request=request, url=request.url, status_code=status, headers={}, body=b"")


async def test_retries_transient_failures_then_succeeds() -> None:
    policy = RetryPolicy(max_attempts=3)
    attempts = 0

    async def fetch(request: Request) -> Response:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise FetchError("boom")
        return _response()

    response = await fetch_with_retry(
        policy, fetch, Request(url="https://example.com"), sleep=_noop_sleep
    )
    assert response.status_code == 200
    assert attempts == 3


async def test_raises_after_max_attempts() -> None:
    policy = RetryPolicy(max_attempts=2)
    attempts = 0

    async def fetch(request: Request) -> Response:
        nonlocal attempts
        attempts += 1
        raise FetchError("boom")

    with pytest.raises(FetchError):
        await fetch_with_retry(policy, fetch, Request(url="https://example.com"), sleep=_noop_sleep)
    assert attempts == 2


async def test_retries_retryable_status() -> None:
    policy = RetryPolicy(max_attempts=3, retryable_statuses=frozenset({500}))
    attempts = 0

    async def fetch(request: Request) -> Response:
        nonlocal attempts
        attempts += 1
        return _response(status=500 if attempts == 1 else 200)

    response = await fetch_with_retry(
        policy, fetch, Request(url="https://example.com"), sleep=_noop_sleep
    )
    assert response.status_code == 200
    assert attempts == 2


async def test_does_not_retry_non_retryable_status() -> None:
    policy = RetryPolicy(max_attempts=3)
    attempts = 0

    async def fetch(request: Request) -> Response:
        nonlocal attempts
        attempts += 1
        return _response(status=404)

    response = await fetch_with_retry(
        policy, fetch, Request(url="https://example.com"), sleep=_noop_sleep
    )
    assert response.status_code == 404
    assert attempts == 1
