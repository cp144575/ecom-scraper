import time

from ecom_scraper.rate_limit.local import DomainRateLimiter, TokenBucket


async def test_token_bucket_limits_rate() -> None:
    bucket = TokenBucket(rate=100, capacity=1)
    start = time.monotonic()
    for _ in range(5):
        await bucket.acquire()
    elapsed = time.monotonic() - start
    assert elapsed >= 0.04


async def test_domain_rate_limiter_is_noop_when_unlimited() -> None:
    limiter = DomainRateLimiter(default_rate=0)
    await limiter.acquire("https://example.com")
