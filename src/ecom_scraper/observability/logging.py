"""Minimal structured logging."""

from structlog.stdlib import BoundLogger
from structlog.stdlib import get_logger as structlog_get_logger


def get_logger(name: str = "ecom_scraper") -> BoundLogger:
    """Return a structured logger bound to the given name."""
    return structlog_get_logger(name)
