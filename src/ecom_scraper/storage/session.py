"""Database engine and session factories."""

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from ecom_scraper.storage.models import Base


def make_engine(database_url: str) -> Engine:
    """Build a SQLAlchemy engine for the given URL."""
    if database_url.startswith("sqlite"):
        return create_engine(database_url, echo=False)
    return create_engine(database_url, echo=False, pool_pre_ping=True)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Build a session factory bound to the given engine."""
    return sessionmaker(bind=engine, expire_on_commit=False)


def create_all(engine: Engine) -> None:
    """Create all tables (development helper; production uses Alembic)."""
    Base.metadata.create_all(engine)
