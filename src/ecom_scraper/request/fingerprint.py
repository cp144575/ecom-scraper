"""Request fingerprint for deduplication."""

from urllib.parse import urlsplit, urlunsplit

from ecom_scraper.request.request import Request


def request_fingerprint(request: Request) -> str:
    """Return a canonical fingerprint used to deduplicate requests."""
    parts = urlsplit(request.url)
    scheme = (parts.scheme or "http").lower()
    netloc = (parts.netloc or "").lower()
    path = parts.path or "/"
    query = "&".join(sorted(parts.query.split("&"))) if parts.query else ""
    normalized = urlunsplit((scheme, netloc, path, query, ""))
    return f"{request.method.upper()} {normalized}"
