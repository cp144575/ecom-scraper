"""Fetcher abstraction."""

from typing import Protocol

from ecom_scraper.request.request import Request
from ecom_scraper.request.response import Response


class Fetcher(Protocol):
    """Fetches a request asynchronously and returns a response."""

    async def fetch(self, request: Request) -> Response:
        """Fetch the request, returning a response or raising FetchError."""
        ...
