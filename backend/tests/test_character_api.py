from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database.connection import get_db_session
from app.main import app


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


def register_and_get_token(
    client: TestClient,
    email: str,
) -> str:
    credentials = {
        "email": email,
        "password": "a-secure-password",
    }
    client.post("/api/auth/register", json=credentials)
    response = client.post(
        "/api/auth/login",
        json=credentials,
    )

    return response.json()["access_token"]

def character_payload() -> dict[str, object]:
    return {
        "name": "Arthur",
        "level": 5,
        "character_class": "Paladin",
        "abilities": {
            "strength": 16,
            "dexterity": 12,
            "constitution": 14,
            "intelligence": 8,
            "wisdom": 10,
            "charisma": 18,
        },
        "saving_throw_proficiencies": [
            "wisdom",
            "charisma",
        ],
        "skill_proficiencies": [
            "athletics",
            "persuasion",
        ],
        "spellcasting_ability": "charisma",
    }


def test_character_api_create_list_and_detail(
    api_client: TestClient,
) -> None:
    token = register_and_get_token(
        api_client,
        "arthur@example.com",
    )
    headers = {
        "Authorization": f"Bearer {token}",
    }
    payload = character_payload()

    create_response = api_client.post(
        "/api/characters",
        json=payload,
        headers=headers,
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"] is not None
    assert created["name"] == "Arthur"
    assert created["proficiency_bonus"] == 3
    assert created["initiative"] == 1
    assert created["passive_perception"] == 10
    assert created["spell_attack_modifier"] == 7
    assert created["spell_save_dc"] == 15
    assert created["ability_modifiers"]["strength"] == 3
    assert created["saving_throw_modifiers"]["charisma"] == 7
    assert created["skill_modifiers"]["athletics"] == 6

    list_response = api_client.get(
        "/api/characters",
        headers=headers,
    )
    detail_response = api_client.get(
        f"/api/characters/{created['id']}",
        headers=headers,
    )

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["id"] == created["id"]

    assert detail_response.status_code == 200
    assert detail_response.json()["id"] == created["id"]

def test_character_api_enforces_ownership_and_validation(
    api_client: TestClient,
) -> None:
    first_token = register_and_get_token(
        api_client,
        "first@example.com",
    )
    second_token = register_and_get_token(
        api_client,
        "second@example.com",
    )
    first_headers = {
        "Authorization": f"Bearer {first_token}",
    }
    second_headers = {
        "Authorization": f"Bearer {second_token}",
    }

    created = api_client.post(
        "/api/characters",
        json=character_payload(),
        headers=first_headers,
    ).json()
    character_id = created["id"]

    second_list = api_client.get(
        "/api/characters",
        headers=second_headers,
    )
    forbidden_detail = api_client.get(
        f"/api/characters/{character_id}",
        headers=second_headers,
    )
    unauthenticated_list = api_client.get(
        "/api/characters"
    )

    invalid_payload = character_payload()
    invalid_payload["skill_proficiencies"] = ["luck"]
    invalid_response = api_client.post(
        "/api/characters",
        json=invalid_payload,
        headers=first_headers,
    )

    blank_name_payload = character_payload()
    blank_name_payload["name"] = "   "
    blank_name_response = api_client.post(
        "/api/characters",
        json=blank_name_payload,
        headers=first_headers,
    )

    assert second_list.status_code == 200
    assert second_list.json() == []
    assert forbidden_detail.status_code == 404
    assert unauthenticated_list.status_code == 401
    assert invalid_response.status_code == 422
    assert blank_name_response.status_code == 422