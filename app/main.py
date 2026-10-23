"""FastAPI application entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends, FastAPI, status
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, engine, get_db, make_get_db
from app.models import Item


class ItemCreate(BaseModel):
    """Validated request body for creating an item."""

    title: str = Field(min_length=1, max_length=200)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title must contain at least one non-space character.")
        return value


class ItemRead(BaseModel):
    """Public item response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    created_at: datetime
    updated_at: datetime


def create_app(database_engine: Engine = engine) -> FastAPI:
    """Build the app, allowing tests to provide an isolated database."""
    if database_engine is engine:
        session_dependency = get_db
    else:
        test_session_factory = sessionmaker(
            bind=database_engine,
            autoflush=False,
            expire_on_commit=False,
        )
        session_dependency = make_get_db(test_session_factory)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        Base.metadata.create_all(bind=database_engine)
        yield

    application = FastAPI(
        title="Student Task Management API",
        version="1.0.0",
        lifespan=lifespan,
    )

    @application.get("/health", tags=["health"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    @application.post(
        "/items",
        response_model=ItemRead,
        status_code=status.HTTP_201_CREATED,
        tags=["items"],
    )
    def create_item(
        payload: ItemCreate,
        session: Session = Depends(session_dependency),
    ) -> Item:
        item = Item(title=payload.title)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

    return application


app = create_app()
