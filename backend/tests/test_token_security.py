from datetime import timedelta

import pytest

from app.security.tokens import (
    create_access_token,
    decode_access_token,
)


def test_access_token_preserves_user_identity() -> None:
    token = create_access_token(user_id=42)

    assert decode_access_token(token) == 42


def test_invalid_access_token_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="invalid access token",
    ):
        decode_access_token("not-a-token")


def test_expired_access_token_is_rejected() -> None:
    token = create_access_token(
        user_id=42,
        expires_delta=timedelta(seconds=-1),
    )

    with pytest.raises(
        ValueError,
        match="invalid access token",
    ):
        decode_access_token(token)