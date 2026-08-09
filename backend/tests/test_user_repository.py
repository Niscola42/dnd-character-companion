from sqlalchemy.orm import Session

from app.repositories.user import UserRepository


def test_user_repository_adds_and_finds_user(
    db_session: Session,
) -> None:
    repository = UserRepository(db_session)

    created_user = repository.add(
        email="arthur@example.com",
        password_hash="hashed-password",
    )
    found_user = repository.get_by_email(
        "arthur@example.com"
    )

    assert created_user.id is not None
    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.email == "arthur@example.com"
    assert found_user.password_hash == "hashed-password"