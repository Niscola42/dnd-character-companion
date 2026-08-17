from io import BytesIO

from fastapi.testclient import TestClient

from tests.test_character_api import (
    character_payload,
    register_and_get_token,
)


def test_character_portrait_api_uploads_image(
    api_client: TestClient,
) -> None:
    token = register_and_get_token(
        api_client,
        "portrait@example.com",
    )
    headers = {
        "Authorization": f"Bearer {token}",
    }

    character = api_client.post(
        "/api/characters",
        json=character_payload(),
        headers=headers,
    ).json()
    character_id = character["id"]

    upload_response = api_client.post(
        f"/api/characters/{character_id}/portrait",
        files={
            "portrait": (
                "arthur.png",
                BytesIO(b"fake-png-content"),
                "image/png",
            ),
        },
        headers=headers,
    )

    assert upload_response.status_code == 200

    uploaded = upload_response.json()

    assert uploaded["portrait_url"].startswith(
        f"/uploads/characters/{character_id}/"
    )

def test_character_portrait_api_enforces_security(
    api_client: TestClient,
) -> None:
    owner_token = register_and_get_token(
        api_client,
        "portrait-owner@example.com",
    )
    other_token = register_and_get_token(
        api_client,
        "portrait-other@example.com",
    )
    owner_headers = {
        "Authorization": f"Bearer {owner_token}",
    }
    other_headers = {
        "Authorization": f"Bearer {other_token}",
    }

    character = api_client.post(
        "/api/characters",
        json=character_payload(),
        headers=owner_headers,
    ).json()
    character_id = character["id"]

    forbidden_response = api_client.post(
        f"/api/characters/{character_id}/portrait",
        files={
            "portrait": (
                "portrait.png",
                BytesIO(b"fake-png-content"),
                "image/png",
            ),
        },
        headers=other_headers,
    )

    invalid_type_response = api_client.post(
        f"/api/characters/{character_id}/portrait",
        files={
            "portrait": (
                "portrait.txt",
                BytesIO(b"not-an-image"),
                "text/plain",
            ),
        },
        headers=owner_headers,
    )

    unauthenticated_response = api_client.post(
        f"/api/characters/{character_id}/portrait",
        files={
            "portrait": (
                "portrait.png",
                BytesIO(b"fake-png-content"),
                "image/png",
            ),
        },
    )

    detail_response = api_client.get(
        f"/api/characters/{character_id}",
        headers=owner_headers,
    )

    assert forbidden_response.status_code == 404
    assert invalid_type_response.status_code == 422
    assert unauthenticated_response.status_code == 401
    assert detail_response.json()["portrait_url"] is None