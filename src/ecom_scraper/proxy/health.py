"""Proxy health tracking."""

from dataclasses import dataclass


@dataclass
class ProxyHealth:
    """Tracks success and failure counts for a proxy."""

    success: int = 0
    failure: int = 0
    last_status: str = "unknown"

    def record_success(self) -> None:
        self.success += 1
        self.last_status = "healthy"

    def record_failure(self) -> None:
        self.failure += 1
        self.last_status = "unhealthy"

    @property
    def healthy(self) -> bool:
        return self.last_status == "healthy"
