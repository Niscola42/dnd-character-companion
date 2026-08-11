from sqlalchemy.orm import Session

from app.domain.character.abilities import AbilityScores
from app.domain.character.character import Character
from app.repositories.character import CharacterRepository
from app.repositories.user import UserRepository
from app.domain.character.health import HitPoints


def make_character(name: str) -> Character:
    return Character(
        name=name,
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
        saving_throw_proficiencies=frozenset(
            {"wisdom", "charisma"}
        ),
        skill_proficiencies=frozenset(
            {"athletics", "persuasion"}
        ),
        spellcasting_ability="charisma",

        hit_points=HitPoints(
            maximum=42,
            current=31,
            temporary=5,
        ),
    )


def test_character_repository_round_trip_and_ownership(
    db_session: Session,
) -> None:
    user_repository = UserRepository(db_session)
    first_user = user_repository.add(
        email="first@example.com",
        password_hash="hash",
    )
    second_user = user_repository.add(
        email="second@example.com",
        password_hash="hash",
    )

    repository = CharacterRepository(db_session)

    created = repository.add(
        owner_id=first_user.id,
        character=make_character("Arthur"),
    )
    repository.add(
        owner_id=second_user.id,
        character=make_character("Lancelot"),
    )

    first_user_characters = repository.list_by_owner(
        first_user.id
    )
    owned_character = repository.get_by_id_and_owner(
        character_id=created.id,
        owner_id=first_user.id,
    )
    forbidden_character = repository.get_by_id_and_owner(
        character_id=created.id,
        owner_id=second_user.id,
    )

    persisted_hit_points = (
        first_user_characters[0].hit_points
    )

    assert persisted_hit_points.maximum == 42
    assert persisted_hit_points.current == 31
    assert persisted_hit_points.temporary == 5

    assert created.id is not None
    assert created.owner_id == first_user.id

    assert len(first_user_characters) == 1
    assert first_user_characters[0].name == "Arthur"
    assert first_user_characters[0].abilities.charisma == 18
    assert first_user_characters[0].skill_proficiencies == (
        frozenset({"athletics", "persuasion"})
    )

    assert owned_character is not None
    assert owned_character.id == created.id
    assert forbidden_character is None