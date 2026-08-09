from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.user import UserModel


class UserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(
        self,
        email: str,
        password_hash: str,
    ) -> UserModel:
        user = UserModel(
            email=email,
            password_hash=password_hash,
        )

        self._session.add(user)
        self._session.flush()

        return user

    def get_by_email(
        self,
        email: str,
    ) -> Optional[UserModel]:
        statement = select(UserModel).where(
            UserModel.email == email
        )

        return self._session.scalar(statement)