"""SQLite engine and SQLAlchemy session configuration."""

import os
from collections.abc import Callable, Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.engine import make_url


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
connect_args = (
    {"check_same_thread": False}
    if make_url(DATABASE_URL).get_backend_name() == "sqlite"
    else {}
)

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""


def make_get_db(
    session_factory: sessionmaker[Session],
) -> Callable[[], Generator[Session, None, None]]:
    """Create a FastAPI-compatible dependency for a session factory."""

    def get_session() -> Generator[Session, None, None]:
        with session_factory() as session:
            yield session

    return get_session


get_db = make_get_db(SessionLocal)
