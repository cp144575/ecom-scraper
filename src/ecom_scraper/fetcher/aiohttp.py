"""Asynchronous HTTP fetcher backed by aiohttp."""

import aiohttp

from ecom_scraper.exceptions import FetchError
from ecom_scraper.request.request import Request
from ecom_scraper.request.response import Response


class AiohttpFetcher:
    """Fetches requests asynchronously using a long-lived aiohttp.ClientSession."""

    def __init__(
        self,
        *,
        timeout: float = 10.0,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._owns_session = session is None
        self._session = session

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession(timeout=self._timeout)
        return self._session

    async def fetch(self, request: Request) -> Response:
        """Fetch the request, wrapping transport and timeout errors as FetchError."""
        session = await self._get_session()
        try:
            async with session.request(
                request.method, request.url, headers=request.headers
            ) as response:
                body = await response.read()
                return Response(
                    request=request,
                    url=str(response.url),
                    status_code=response.status,
                    headers=dict(response.headers),
                    body=body,
                )
        except (aiohttp.ClientError, TimeoutError) as exc:
            raise FetchError(f"Failed to fetch {request.url}") from exc

    async def close(self) -> None:
        """Release the underlying session when it was created by this fetcher."""
        if self._owns_session and self._session is not None:
            await self._session.close()
            self._session = None
