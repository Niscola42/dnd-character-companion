from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from app.database.connection import get_db_session
from app.database.models.user import UserModel
from app.repositories.user import UserRepository
from app.security.tokens import decode_access_token


bearer_scheme = HTTPBearer(auto_error=False)


def unauthorized_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    credentials: Optional[
        HTTPAuthorizationCredentials
    ] = Depends(bearer_scheme),
    session: Session = Depends(get_db_session),
) -> UserModel:
    if credentials is None:
        raise unauthorized_error()

    try:
        user_id = decode_access_token(
            credentials.credentials
        )
    except ValueError as error:
        raise unauthorized_error() from error

    user = UserRepository(session).get_by_id(user_id)

    if user is None:
        raise unauthorized_error()

    return user