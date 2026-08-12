from collections.abc import Iterator

import pytest
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient

from app.database.connection import (
    engine,
    get_db_session,
)
from app.main import app



@pytest.fixture
def db_session() -> Iterator[Session]:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def api_client(
    db_session: Session,
) -> Iterator[TestClient]:
    def override_session() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_db_session] = (
        override_session
    )

    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()