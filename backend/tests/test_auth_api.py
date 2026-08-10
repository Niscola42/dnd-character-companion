from collections.abc import Iterator

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database.connection import get_db_session
from app.main import app
from app.security.tokens import decode_access_token


def test_auth_api_registers_and_logs_in(
    db_session: Session,
) -> None:
    def override_session() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_db_session] = (
        override_session
    )
    client = TestClient(app)

    try:
        register_response = client.post(
            "/api/auth/register",
            json={
                "email": "arthur@example.com",
                "password": "a-secure-password",
            },
        )
        login_response = client.post(
            "/api/auth/login",
            json={
                "email": "arthur@example.com",
                "password": "a-secure-password",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert register_response.status_code == 201
    assert register_response.json()["email"] == (
        "arthur@example.com"
    )
    assert "password" not in register_response.json()
    assert "password_hash" not in register_response.json()

    assert login_response.status_code == 200
    token_data = login_response.json()
    assert token_data["token_type"] == "bearer"
    assert decode_access_token(
        token_data["access_token"]
    ) == register_response.json()["id"]

def test_auth_api_protects_current_user(
    db_session: Session,
) -> None:
    def override_session() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_db_session] = (
        override_session
    )
    client = TestClient(app)

    try:
        register_response = client.post(
            "/api/auth/register",
            json={
                "email": "arthur@example.com",
                "password": "a-secure-password",
            },
        )
        duplicate_response = client.post(
            "/api/auth/register",
            json={
                "email": "ARTHUR@example.com",
                "password": "another-password",
            },
        )
        invalid_login_response = client.post(
            "/api/auth/login",
            json={
                "email": "arthur@example.com",
                "password": "wrong-password",
            },
        )
        login_response = client.post(
            "/api/auth/login",
            json={
                "email": "arthur@example.com",
                "password": "a-secure-password",
            },
        )
        token = login_response.json()["access_token"]

        current_user_response = client.get(
            "/api/auth/me",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        missing_token_response = client.get(
            "/api/auth/me"
        )
        invalid_token_response = client.get(
            "/api/auth/me",
            headers={
                "Authorization": "Bearer invalid-token",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert register_response.status_code == 201
    assert duplicate_response.status_code == 409
    assert invalid_login_response.status_code == 401

    assert current_user_response.status_code == 200
    assert current_user_response.json()["email"] == (
        "arthur@example.com"
    )

    assert missing_token_response.status_code == 401
    assert invalid_token_response.status_code == 401

def test_auth_api_validates_registration_input(
    db_session: Session,
) -> None:
    def override_session() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_db_session] = (
        override_session
    )
    client = TestClient(app)

    try:
        invalid_email_response = client.post(
            "/api/auth/register",
            json={
                "email": "not-an-email",
                "password": "a-secure-password",
            },
        )
        short_password_response = client.post(
            "/api/auth/register",
            json={
                "email": "arthur@example.com",
                "password": "short",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert invalid_email_response.status_code == 422
    assert short_password_response.status_code == 422