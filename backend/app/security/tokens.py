from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from jwt.exceptions import InvalidTokenError

from app.config import settings


def create_access_token(
    user_id: int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    now = datetime.now(timezone.utc)
    expiration = now + (
        expires_delta
        or timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": expiration,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        subject = payload.get("sub")

        if subject is None:
            raise ValueError

        return int(subject)
    except (
        InvalidTokenError,
        TypeError,
        ValueError,
    ) as error:
        raise ValueError(
            "invalid access token"
        ) from error