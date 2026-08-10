from app.database.models.user import UserModel
from app.repositories.user import UserRepository
from app.security.passwords import (
    hash_password,
    verify_password,
)


class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class AuthenticationService:
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self._user_repository = user_repository

    def register(
        self,
        email: str,
        password: str,
    ) -> UserModel:
        normalized_email = email.strip().lower()
        existing_user = self._user_repository.get_by_email(
            normalized_email
        )

        if existing_user is not None:
            raise EmailAlreadyRegisteredError

        return self._user_repository.add(
            email=normalized_email,
            password_hash=hash_password(password),
        )

    def authenticate(
        self,
        email: str,
        password: str,
    ) -> UserModel:
        normalized_email = email.strip().lower()
        user = self._user_repository.get_by_email(
            normalized_email
        )

        if user is None:
            raise InvalidCredentialsError

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise InvalidCredentialsError

        return user