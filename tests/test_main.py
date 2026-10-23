"""Integration tests for the FastAPI application."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from app.main import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    test_app = create_app(test_engine)
    with TestClient(test_app) as test_client:
        yield test_client
    test_engine.dispose()


def test_health_check_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_item_returns_persisted_item(client: TestClient) -> None:
    response = client.post("/items", json={"title": "Read chapter"})

    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["title"] == "Read chapter"
    assert body["created_at"]
    assert body["updated_at"]


def test_create_item_rejects_blank_title(client: TestClient) -> None:
    response = client.post("/items", json={"title": "   "})

    assert response.status_code == 422
