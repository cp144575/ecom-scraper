"""Shared pytest fixtures."""

from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from ecom_scraper.storage.models import Base
from ecom_scraper.storage.repository import ProductRepository


@pytest.fixture()
def session_factory() -> Iterator[sessionmaker[Session]]:
    """Provide an isolated in-memory SQLite session factory."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine, expire_on_commit=False)
    engine.dispose()


@pytest.fixture()
def repository(session_factory: sessionmaker[Session]) -> ProductRepository:
    """Provide a product repository backed by in-memory SQLite."""
    return ProductRepository(session_factory)
