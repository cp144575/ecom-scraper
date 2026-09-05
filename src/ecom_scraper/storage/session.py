"""Async database engine and session factories."""

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ecom_scraper.storage.models import Base


def make_async_engine(database_url: str) -> AsyncEngine:
    """Build an async SQLAlchemy engine for the given URL."""
    return create_async_engine(database_url, echo=False, pool_pre_ping=True)


def create_async_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Build an async session factory bound to the given engine."""
    return async_sessionmaker(engine, expire_on_commit=False)


async def create_all_async(engine: AsyncEngine) -> None:
    """Create all tables (development helper; production uses Alembic)."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
