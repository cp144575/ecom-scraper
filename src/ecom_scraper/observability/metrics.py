"""Prometheus metrics for the crawler."""

from prometheus_client import REGISTRY, Counter, generate_latest

crawler_requests_total = Counter(
    "crawler_requests_total",
    "Total crawl requests by outcome.",
    ["status"],
)

crawler_items_total = Counter(
    "crawler_items_total",
    "Total parsed items.",
)


def render_metrics() -> bytes:
    """Render the process metrics in Prometheus text format."""
    return generate_latest(REGISTRY)
