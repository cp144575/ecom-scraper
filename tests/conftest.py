"""Shared pytest fixtures."""

from collections.abc import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from ecom_scraper.storage.models import Base
from ecom_scraper.storage.repository import AsyncProductRepository


@pytest.fixture()
async def session_factory() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    """Provide an isolated in-memory async SQLite session factory."""
    engine = create_async_engine("sqlite+aiosqlite://", poolclass=StaticPool)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield async_sessionmaker(engine, expire_on_commit=False)
    await engine.dispose()


@pytest.fixture()
async def repository(session_factory: async_sessionmaker[AsyncSession]) -> AsyncProductRepository:
    """Provide an async product repository backed by in-memory SQLite."""
    return AsyncProductRepository(session_factory)
