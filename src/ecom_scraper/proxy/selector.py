"""Proxy selection strategies."""

import itertools
from collections.abc import Iterator

from ecom_scraper.proxy.base import Proxy
from ecom_scraper.proxy.pool import ProxyPool


class RoundRobinSelector:
    """Selects proxies in round-robin order within a policy."""

    def __init__(self, pool: ProxyPool) -> None:
        self._pool = pool
        self._iterators: dict[str, Iterator[Proxy]] = {}

    def select(self, policy: str) -> Proxy | None:
        """Return the next proxy for the policy, or None when unavailable."""
        proxies = self._pool.by_policy(policy)
        if not proxies:
            return None
        if policy not in self._iterators:
            self._iterators[policy] = itertools.cycle(proxies)
        return next(self._iterators[policy])
