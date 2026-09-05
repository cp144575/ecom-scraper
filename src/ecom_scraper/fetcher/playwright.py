"""Browser-backed fetcher using Playwright."""

from ecom_scraper.browser.manager import BrowserManager
from ecom_scraper.exceptions import FetchError
from ecom_scraper.request.request import Request
from ecom_scraper.request.response import Response


class PlaywrightFetcher:
    """Fetches pages by rendering them in a headless browser."""

    def __init__(self, manager: BrowserManager, *, timeout_ms: int = 30000) -> None:
        self._manager = manager
        self._timeout_ms = timeout_ms

    async def fetch(self, request: Request) -> Response:
        """Render the request URL and return the resulting HTML."""
        try:
            html = await self._manager.fetch_html(request.url, timeout_ms=self._timeout_ms)
        except Exception as exc:
            raise FetchError(f"Failed to fetch {request.url}") from exc
        return Response(
            request=request,
            url=request.url,
            status_code=200,
            headers={},
            body=html.encode("utf-8"),
        )
