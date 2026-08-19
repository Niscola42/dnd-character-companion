from fastapi.testclient import TestClient


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
        "species": "Human",
        "background": "Soldier",
        "abilities": {
            "strength": 16,
            "dexterity": 12,
            "constitution": 14,
            "intelligence": 8,
            "wisdom": 10,
            "charisma": 18,
        },
        "hit_points": {
            "maximum": 42,
            "current": 31,
            "temporary": 5,
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
    assert created["species"] == "Human"
    assert created["background"] == "Soldier"
    assert created["hit_points"] == {
        "maximum": 42,
        "current": 31,
        "temporary": 5,
    }
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

    forbidden_update = api_client.put(
        f"/api/characters/{character_id}",
        json=character_payload(),
        headers=second_headers,
    )
    forbidden_delete = api_client.delete(
        f"/api/characters/{character_id}",
        headers=second_headers,
    )
    owner_still_has_character = api_client.get(
        f"/api/characters/{character_id}",
        headers=first_headers,
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
    blank_species_payload = character_payload()
    blank_species_payload["species"] = "   "
    blank_species_response = api_client.post(
        "/api/characters",
        json=blank_species_payload,
        headers=first_headers,
    )

    blank_background_payload = character_payload()
    blank_background_payload["background"] = "   "
    blank_background_response = api_client.post(
        "/api/characters",
        json=blank_background_payload,
        headers=first_headers,
    )

    assert forbidden_update.status_code == 404
    assert forbidden_delete.status_code == 404
    assert owner_still_has_character.status_code == 200
    assert second_list.status_code == 200
    assert second_list.json() == []
    assert forbidden_detail.status_code == 404
    assert unauthenticated_list.status_code == 401
    assert invalid_response.status_code == 422
    assert blank_name_response.status_code == 422
    assert blank_species_response.status_code == 422
    assert blank_background_response.status_code == 422

def test_character_api_update_and_delete(
    api_client: TestClient,
) -> None:
    token = register_and_get_token(
        api_client,
        "editor@example.com",
    )
    headers = {
        "Authorization": f"Bearer {token}",
    }

    created = api_client.post(
        "/api/characters",
        json=character_payload(),
        headers=headers,
    ).json()
    character_id = created["id"]

    updated_payload = character_payload()
    updated_payload["name"] = "Arthur Pendragon"
    updated_payload["level"] = 4
    updated_payload["abilities"] = {
        **updated_payload["abilities"],
        "strength": 18,
    }

    update_response = api_client.put(
        f"/api/characters/{character_id}",
        json=updated_payload,
        headers=headers,
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["name"] == "Arthur Pendragon"
    assert updated["level"] == 4
    assert updated["abilities"]["strength"] == 18
    assert updated["ability_modifiers"]["strength"] == 4
    assert updated["proficiency_bonus"] == 2

    delete_response = api_client.delete(
        f"/api/characters/{character_id}",
        headers=headers,
    )
    detail_after_delete = api_client.get(
        f"/api/characters/{character_id}",
        headers=headers,
    )
    list_after_delete = api_client.get(
        "/api/characters",
        headers=headers,
    )

    assert delete_response.status_code == 204
    assert detail_after_delete.status_code == 404
    assert list_after_delete.json() == []

def test_character_api_manages_hit_points(
    api_client: TestClient,
) -> None:
    token = register_and_get_token(
        api_client,
        "healer@example.com",
    )
    headers = {
        "Authorization": f"Bearer {token}",
    }

    created = api_client.post(
        "/api/characters",
        json=character_payload(),
        headers=headers,
    ).json()
    character_id = created["id"]

    damage_response = api_client.post(
        f"/api/characters/{character_id}/health/damage",
        json={"amount": 8},
        headers=headers,
    )

    assert damage_response.status_code == 200
    assert damage_response.json()["hit_points"] == {
        "maximum": 42,
        "current": 28,
        "temporary": 0,
    }

    healing_response = api_client.post(
        f"/api/characters/{character_id}/health/heal",
        json={"amount": 10},
        headers=headers,
    )

    assert healing_response.status_code == 200
    assert healing_response.json()["hit_points"] == {
        "maximum": 42,
        "current": 38,
        "temporary": 0,
    }

    temporary_response = api_client.post(
        f"/api/characters/{character_id}/health/temporary",
        json={"amount": 7},
        headers=headers,
    )

    assert temporary_response.status_code == 200
    assert temporary_response.json()["hit_points"] == {
        "maximum": 42,
        "current": 38,
        "temporary": 7,
    }

    detail_response = api_client.get(
        f"/api/characters/{character_id}",
        headers=headers,
    )

    assert detail_response.json()["hit_points"] == {
        "maximum": 42,
        "current": 38,
        "temporary": 7,
    }

def test_character_api_protects_hit_point_actions(
    api_client: TestClient,
) -> None:
    owner_token = register_and_get_token(
        api_client,
        "hp-owner@example.com",
    )
    other_token = register_and_get_token(
        api_client,
        "hp-other@example.com",
    )
    owner_headers = {
        "Authorization": f"Bearer {owner_token}",
    }
    other_headers = {
        "Authorization": f"Bearer {other_token}",
    }

    created = api_client.post(
        "/api/characters",
        json=character_payload(),
        headers=owner_headers,
    ).json()
    character_id = created["id"]

    forbidden_response = api_client.post(
        f"/api/characters/{character_id}/health/damage",
        json={"amount": 1},
        headers=other_headers,
    )
    negative_response = api_client.post(
        f"/api/characters/{character_id}/health/damage",
        json={"amount": -1},
        headers=owner_headers,
    )
    unknown_response = api_client.post(
        f"/api/characters/{character_id}/health/unknown",
        json={"amount": 1},
        headers=owner_headers,
    )
    unauthenticated_response = api_client.post(
        f"/api/characters/{character_id}/health/heal",
        json={"amount": 1},
    )

    detail_response = api_client.get(
        f"/api/characters/{character_id}",
        headers=owner_headers,
    )

    assert forbidden_response.status_code == 404
    assert negative_response.status_code == 422
    assert unknown_response.status_code == 422
    assert unauthenticated_response.status_code == 401

    assert detail_response.json()["hit_points"] == {
        "maximum": 42,
        "current": 31,
        "temporary": 5,
    }

