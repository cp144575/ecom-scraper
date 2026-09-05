"""Retry policy with exponential backoff and jitter."""

import asyncio
import random
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from ecom_scraper.exceptions import FetchError
from ecom_scraper.request.request import Request
from ecom_scraper.request.response import Response

_DEFAULT_RETRYABLE_STATUSES = frozenset({429, 500, 502, 503, 504})


@dataclass(frozen=True)
class RetryPolicy:
    """Controls how failed or retryable requests are retried."""

    max_attempts: int = 3
    retryable_statuses: frozenset[int] = _DEFAULT_RETRYABLE_STATUSES
    backoff_base: float = 0.5
    backoff_factor: float = 2.0
    jitter: float = 0.1
    backoff_max: float = 30.0

    def delay_for(self, attempt: int) -> float:
        """Return the delay before the given attempt (1-based)."""
        delay = self.backoff_base * (self.backoff_factor ** (attempt - 1))
        if self.jitter:
            delay *= 1.0 + random.uniform(-self.jitter, self.jitter)
        return max(0.0, min(delay, self.backoff_max))


async def fetch_with_retry(
    policy: RetryPolicy,
    fetch: Callable[[Request], Awaitable[Response]],
    request: Request,
    *,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> Response:
    """Fetch a request, retrying transient failures and retryable statuses."""
    response: Response | None = None
    for attempt in range(1, policy.max_attempts + 1):
        try:
            response = await fetch(request)
        except FetchError:
            if attempt >= policy.max_attempts:
                raise
            await sleep(policy.delay_for(attempt))
            continue
        if response.status_code in policy.retryable_statuses and attempt < policy.max_attempts:
            await sleep(policy.delay_for(attempt))
            continue
        return response
    assert response is not None
    return response
