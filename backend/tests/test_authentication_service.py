import pytest
from sqlalchemy.orm import Session

from app.repositories.user import UserRepository
from app.services.authentication import (
    AuthenticationService,
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
)
from app.security.passwords import verify_password


def test_authentication_service_registers_and_logs_in(
    db_session: Session,
) -> None:
    repository = UserRepository(db_session)
    service = AuthenticationService(repository)

    created_user = service.register(
        email="Arthur@Example.com",
        password="a-secure-password",
    )
    authenticated_user = service.authenticate(
        email="arthur@example.com",
        password="a-secure-password",
    )

    assert created_user.email == "arthur@example.com"
    assert created_user.password_hash != "a-secure-password"
    assert verify_password(
        "a-secure-password",
        created_user.password_hash,
    )
    assert authenticated_user.id == created_user.id


def test_authentication_service_rejects_duplicate_email(
    db_session: Session,
) -> None:
    service = AuthenticationService(
        UserRepository(db_session)
    )
    service.register(
        email="arthur@example.com",
        password="a-secure-password",
    )

    with pytest.raises(EmailAlreadyRegisteredError):
        service.register(
            email="ARTHUR@example.com",
            password="another-password",
        )


def test_authentication_service_rejects_invalid_credentials(
    db_session: Session,
) -> None:
    service = AuthenticationService(
        UserRepository(db_session)
    )
    service.register(
        email="arthur@example.com",
        password="a-secure-password",
    )

    with pytest.raises(InvalidCredentialsError):
        service.authenticate(
            email="arthur@example.com",
            password="wrong-password",
        )

    with pytest.raises(InvalidCredentialsError):
        service.authenticate(
            email="missing@example.com",
            password="a-secure-password",
        )