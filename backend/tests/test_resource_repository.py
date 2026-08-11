from sqlalchemy.orm import Session

from app.domain.character.abilities import AbilityScores
from app.domain.character.character import Character
from app.domain.resource.resource import (
    RecoveryType,
    Resource,
)
from app.repositories.character import CharacterRepository
from app.repositories.resource import ResourceRepository
from app.repositories.user import UserRepository


def test_resource_repository_round_trip_and_ownership(
    db_session: Session,
) -> None:
    user_repository = UserRepository(db_session)
    first_user = user_repository.add(
        email="resource-owner@example.com",
        password_hash="hash",
    )
    second_user = user_repository.add(
        email="other-owner@example.com",
        password_hash="hash",
    )

    character = CharacterRepository(db_session).add(
        owner_id=first_user.id,
        character=Character(
            name="Arthur",
            level=5,
            character_class="Paladin",
            abilities=AbilityScores(
                strength=16,
                dexterity=12,
                constitution=14,
                intelligence=8,
                wisdom=10,
                charisma=18,
            ),
        ),
    )

    repository = ResourceRepository(db_session)
    created = repository.add(
        character_id=character.id,
        owner_id=first_user.id,
        resource=Resource(
            name="Lay on Hands",
            source="Paladin",
            maximum=25,
            current=18,
            recovery_type=RecoveryType.LONG_REST,
        ),
    )

    owner_resources = repository.list_by_character(
        character_id=character.id,
        owner_id=first_user.id,
    )
    forbidden_resources = repository.list_by_character(
        character_id=character.id,
        owner_id=second_user.id,
    )

    assert created is not None
    assert created.id is not None
    assert created.character_id == character.id
    assert created.name == "Lay on Hands"

    assert len(owner_resources) == 1
    assert owner_resources[0].current == 18
    assert forbidden_resources == []

    loaded = repository.get_by_id_and_owner(
        resource_id=created.id,
        owner_id=first_user.id,
    )
    forbidden = repository.get_by_id_and_owner(
        resource_id=created.id,
        owner_id=second_user.id,
    )

    assert loaded is not None
    assert loaded.current == 18
    assert forbidden is None

    loaded.consume(3)

    updated = repository.update_by_id_and_owner(
        resource_id=created.id,
        owner_id=first_user.id,
        resource=loaded,
    )

    assert updated is not None
    assert updated.current == 15

    forbidden_delete = (
        repository.delete_by_id_and_owner(
            resource_id=created.id,
            owner_id=second_user.id,
        )
    )

    assert forbidden_delete is False

    deleted = repository.delete_by_id_and_owner(
        resource_id=created.id,
        owner_id=first_user.id,
    )

    assert deleted is True
    assert repository.list_by_character(
        character_id=character.id,
        owner_id=first_user.id,
    ) == []