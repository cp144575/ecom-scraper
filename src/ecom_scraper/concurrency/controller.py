"""Concurrency controller enforcing global and per-domain limits."""

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from urllib.parse import urlsplit


class ConcurrencyController:
    """Bounds concurrent fetches globally and per domain."""

    def __init__(
        self,
        *,
        global_limit: int,
        domain_limits: dict[str, int] | None = None,
        default_domain_limit: int | None = None,
    ) -> None:
        self.global_limit = global_limit
        self._global = asyncio.Semaphore(global_limit)
        self._domain_limits = domain_limits or {}
        self._default_domain_limit = default_domain_limit
        self._domain_semaphores: dict[str, asyncio.Semaphore] = {}

    def _semaphore_for(self, domain: str) -> asyncio.Semaphore | None:
        limit = self._domain_limits.get(domain, self._default_domain_limit)
        if limit is None:
            return None
        if domain not in self._domain_semaphores:
            self._domain_semaphores[domain] = asyncio.Semaphore(limit)
        return self._domain_semaphores[domain]

    @asynccontextmanager
    async def acquire(self, url: str) -> AsyncIterator[None]:
        """Hold a global slot and, when configured, a domain slot."""
        domain = (urlsplit(url).netloc or "default").lower()
        async with self._global:
            semaphore = self._semaphore_for(domain)
            if semaphore is None:
                yield
            else:
                async with semaphore:
                    yield
