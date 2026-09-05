"""HTTP response value object."""

from dataclasses import dataclass

from ecom_scraper.request.request import Request


@dataclass(frozen=True, slots=True)
class Response:
    """An HTTP response associated with its originating request."""

    request: Request
    url: str
    status_code: int
    headers: dict[str, str]
    body: bytes
