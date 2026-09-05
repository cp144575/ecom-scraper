"""Shared pytest fixtures."""

import os
import tempfile
from collections.abc import AsyncIterator

import pytest
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ecom_scraper.storage.models import Base
from ecom_scraper.storage.repository import AsyncProductRepository


@pytest.fixture()
async def session_factory() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    """Provide an isolated file-backed async SQLite session factory."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    engine = create_async_engine(f"sqlite+aiosqlite:///{path}", pool_pre_ping=True)

    @event.listens_for(engine.sync_engine, "connect")
    def _set_sqlite_pragma(dbapi_connection: object, connection_record: object) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA busy_timeout=5000")
        cursor.close()

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield async_sessionmaker(engine, expire_on_commit=False)
    await engine.dispose()
    os.unlink(path)


@pytest.fixture()
async def repository(session_factory: async_sessionmaker[AsyncSession]) -> AsyncProductRepository:
    """Provide an async product repository backed by SQLite."""
    return AsyncProductRepository(session_factory)
