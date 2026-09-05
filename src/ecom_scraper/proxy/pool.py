"""In-memory proxy pool."""

from ecom_scraper.proxy.base import Proxy


class ProxyPool:
    """Holds a set of proxies and exposes them by policy."""

    def __init__(self, proxies: list[Proxy] | None = None) -> None:
        self._proxies: list[Proxy] = list(proxies or [])

    def add(self, proxy: Proxy) -> None:
        """Register a proxy."""
        self._proxies.append(proxy)

    def by_policy(self, policy: str) -> list[Proxy]:
        """Return proxies tagged with the given policy."""
        return [proxy for proxy in self._proxies if proxy.policy == policy]

    def __len__(self) -> int:
        return len(self._proxies)
