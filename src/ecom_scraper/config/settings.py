"""Runtime configuration loaded from environment variables."""

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    """Application settings with environment-based defaults."""

    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///ecom_scraper.db")
    sync_database_url: str = os.getenv("SYNC_DATABASE_URL", "sqlite:///ecom_scraper.db")
    redis_url: str = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    request_timeout: float = float(os.getenv("REQUEST_TIMEOUT", "10.0"))
    concurrency_global: int = int(os.getenv("CONCURRENCY_GLOBAL", "100"))
    concurrency_domain_default: int = int(os.getenv("CONCURRENCY_DOMAIN_DEFAULT", "20"))
    queue_maxsize: int = int(os.getenv("QUEUE_MAXSIZE", "0"))

    retry_max_attempts: int = int(os.getenv("RETRY_MAX_ATTEMPTS", "3"))
    retry_backoff_base: float = float(os.getenv("RETRY_BACKOFF_BASE", "0.5"))
    retry_jitter: float = float(os.getenv("RETRY_JITTER", "0.1"))

    rate_limit_rps: float = float(os.getenv("RATE_LIMIT_RPS", "0"))
