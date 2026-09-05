"""Synchronous HTTP fetcher backed by httpx."""

import httpx

from ecom_scraper.exceptions import FetchError
from ecom_scraper.request.request import Request
from ecom_scraper.request.response import Response


class HttpxFetcher:
    """Fetches requests synchronously using a long-lived httpx.Client."""

    def __init__(self, *, timeout: float = 10.0, client: httpx.Client | None = None) -> None:
        self._timeout = timeout
        self._owns_client = client is None
        self._client = client or httpx.Client(timeout=timeout, follow_redirects=True)

    def fetch(self, request: Request) -> Response:
        try:
            http_response = self._client.request(
                request.method,
                request.url,
                headers=request.headers,
            )
        except httpx.HTTPError as exc:
            raise FetchError(f"Failed to fetch {request.url}") from exc

        return Response(
            request=request,
            url=str(http_response.url),
            status_code=http_response.status_code,
            headers=dict(http_response.headers),
            body=http_response.content,
        )

    def close(self) -> None:
        """Release the underlying client when it was created by this fetcher."""
        if self._owns_client:
            self._client.close()
