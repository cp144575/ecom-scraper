"""Runtime configuration loaded from environment variables."""

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    """Application settings with environment-based defaults."""

    database_url: str = os.getenv("DATABASE_URL", "sqlite:///ecom_scraper.db")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
