from fastapi.testclient import TestClient

from tests.test_character_api import (
    character_payload,
    register_and_get_token,
)


def test_resource_api_creates_and_lists_resources(
    api_client: TestClient,
) -> None:
    token = register_and_get_token(
        api_client,
        "resource-api@example.com",
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

    create_response = api_client.post(
        f"/api/characters/{character_id}/resources",
        json={
            "name": "Lay on Hands",
            "source": "Paladin",
            "maximum": 25,
            "current": 18,
            "recovery_type": "LONG_REST",
            "metadata": {
                "description": "Healing pool",
            },
        },
        headers=headers,
    )

    assert create_response.status_code == 201
    created = create_response.json()

    assert created["id"] is not None
    assert created["character_id"] == character_id
    assert created["name"] == "Lay on Hands"
    assert created["source"] == "Paladin"
    assert created["maximum"] == 25
    assert created["current"] == 18
    assert created["recovery_type"] == "LONG_REST"
    assert created["metadata"] == {
        "description": "Healing pool",
    }

    list_response = api_client.get(
        f"/api/characters/{character_id}/resources",
        headers=headers,
    )

    assert list_response.status_code == 200
    assert list_response.json() == [created]

def test_resource_api_consumes_and_restores_resource(
    api_client: TestClient,
) -> None:
    token = register_and_get_token(
        api_client,
        "resource-actions@example.com",
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

    resource = api_client.post(
        f"/api/characters/{character_id}/resources",
        json={
            "name": "Lay on Hands",
            "source": "Paladin",
            "maximum": 25,
            "current": 18,
            "recovery_type": "LONG_REST",
        },
        headers=headers,
    ).json()
    resource_id = resource["id"]

    consume_response = api_client.post(
        (
            f"/api/characters/{character_id}"
            f"/resources/{resource_id}/consume"
        ),
        json={"amount": 5},
        headers=headers,
    )

    assert consume_response.status_code == 200
    assert consume_response.json()["current"] == 13

    restore_response = api_client.post(
        (
            f"/api/characters/{character_id}"
            f"/resources/{resource_id}/restore"
        ),
        json={"amount": 20},
        headers=headers,
    )

    assert restore_response.status_code == 200
    assert restore_response.json()["current"] == 25

    list_response = api_client.get(
        f"/api/characters/{character_id}/resources",
        headers=headers,
    )

    assert list_response.json()[0]["current"] == 25


def test_resource_api_protects_resource_actions(
    api_client: TestClient,
) -> None:
    owner_token = register_and_get_token(
        api_client,
        "resource-owner-api@example.com",
    )
    other_token = register_and_get_token(
        api_client,
        "resource-other-api@example.com",
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

    resource = api_client.post(
        f"/api/characters/{character_id}/resources",
        json={
            "name": "Divine Channel",
            "source": "Paladin",
            "maximum": 2,
            "current": 1,
            "recovery_type": "SHORT_REST",
        },
        headers=owner_headers,
    ).json()
    resource_id = resource["id"]

    forbidden_list = api_client.get(
        f"/api/characters/{character_id}/resources",
        headers=other_headers,
    )
    forbidden_action = api_client.post(
        (
            f"/api/characters/{character_id}"
            f"/resources/{resource_id}/restore"
        ),
        json={"amount": 1},
        headers=other_headers,
    )
    excessive_consumption = api_client.post(
        (
            f"/api/characters/{character_id}"
            f"/resources/{resource_id}/consume"
        ),
        json={"amount": 2},
        headers=owner_headers,
    )
    negative_amount = api_client.post(
        (
            f"/api/characters/{character_id}"
            f"/resources/{resource_id}/restore"
        ),
        json={"amount": -1},
        headers=owner_headers,
    )

    owner_list = api_client.get(
        f"/api/characters/{character_id}/resources",
        headers=owner_headers,
    )

    assert forbidden_list.status_code == 200
    assert forbidden_list.json() == []
    assert forbidden_action.status_code == 404
    assert excessive_consumption.status_code == 422
    assert negative_amount.status_code == 422

    assert owner_list.json()[0]["current"] == 1

def test_rest_api_restores_character_resources(
    api_client: TestClient,
) -> None:
    token = register_and_get_token(
        api_client,
        "rest-api@example.com",
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

    short_rest_resource = api_client.post(
        f"/api/characters/{character_id}/resources",
        json={
            "name": "Channel Divinity",
            "source": "Paladin",
            "maximum": 2,
            "current": 0,
            "recovery_type": "SHORT_REST",
        },
        headers=headers,
    ).json()

    long_rest_resource = api_client.post(
        f"/api/characters/{character_id}/resources",
        json={
            "name": "Lay on Hands",
            "source": "Paladin",
            "maximum": 25,
            "current": 8,
            "recovery_type": "LONG_REST",
        },
        headers=headers,
    ).json()

    short_rest_response = api_client.post(
        f"/api/characters/{character_id}/rests",
        json={"rest_type": "SHORT"},
        headers=headers,
    )

    assert short_rest_response.status_code == 200
    short_summary = short_rest_response.json()

    assert short_summary["changes"] == [
        {
            "name": "Channel Divinity",
            "before": 0,
            "after": 2,
        }
    ]
    assert short_summary["hit_points"] is None

    resources_after_short_rest = api_client.get(
        f"/api/characters/{character_id}/resources",
        headers=headers,
    ).json()

    resources_by_id = {
        resource["id"]: resource
        for resource in resources_after_short_rest
    }

    assert resources_by_id[
        short_rest_resource["id"]
    ]["current"] == 2
    assert resources_by_id[
        long_rest_resource["id"]
    ]["current"] == 8

    long_rest_response = api_client.post(
        f"/api/characters/{character_id}/rests",
        json={"rest_type": "LONG"},
        headers=headers,
    )

    assert long_rest_response.status_code == 200
    long_summary = long_rest_response.json()

    assert long_summary["changes"] == [
        {
            "name": "Lay on Hands",
            "before": 8,
            "after": 25,
        }
    ]
    assert long_summary["hit_points"] == {
        "current_before": 31,
        "current_after": 42,
        "temporary_before": 5,
        "temporary_after": 0,
    }

    detail_response = api_client.get(
        f"/api/characters/{character_id}",
        headers=headers,
    )

    assert detail_response.json()["hit_points"] == {
        "maximum": 42,
        "current": 42,
        "temporary": 0,
    }

def test_rest_api_enforces_ownership_and_validation(
    api_client: TestClient,
) -> None:
    owner_token = register_and_get_token(
        api_client,
        "rest-owner@example.com",
    )
    other_token = register_and_get_token(
        api_client,
        "rest-other@example.com",
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
        f"/api/characters/{character_id}/rests",
        json={"rest_type": "LONG"},
        headers=other_headers,
    )
    invalid_response = api_client.post(
        f"/api/characters/{character_id}/rests",
        json={"rest_type": "WEEKEND"},
        headers=owner_headers,
    )
    unauthenticated_response = api_client.post(
        f"/api/characters/{character_id}/rests",
        json={"rest_type": "SHORT"},
    )

    detail_response = api_client.get(
        f"/api/characters/{character_id}",
        headers=owner_headers,
    )

    assert forbidden_response.status_code == 404
    assert invalid_response.status_code == 422
    assert unauthenticated_response.status_code == 401

    assert detail_response.json()["hit_points"] == {
        "maximum": 42,
        "current": 31,
        "temporary": 5,
    }