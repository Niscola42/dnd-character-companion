import pytest
from app.domain.character.abilities import AbilityScores
from app.domain.character.character import Character


def test_character_stores_core_information() -> None:
    abilities = AbilityScores(
        strength=16,
        dexterity=12,
        constitution=14,
        intelligence=8,
        wisdom=10,
        charisma=18,
    )

    character = Character(
        name="Arthur",
        level=5,
        character_class="Paladin",
        abilities=abilities,
    )

    assert character.name == "Arthur"
    assert character.level == 5
    assert character.character_class == "Paladin"
    assert character.abilities == abilities

@pytest.mark.parametrize("invalid_level", [0, 6])
def test_character_rejects_level_outside_mvp(
    invalid_level: int,
) -> None:
    abilities = AbilityScores(
        strength=10,
        dexterity=10,
        constitution=10,
        intelligence=10,
        wisdom=10,
        charisma=10,
    )

    with pytest.raises(
        ValueError,
        match="level must be between 1 and 5",
    ):
        Character(
            name="Arthur",
            level=invalid_level,
            character_class="Paladin",
            abilities=abilities,
        )

@pytest.mark.parametrize("invalid_name", ["", "   "])
def test_character_rejects_blank_name(
    invalid_name: str,
) -> None:
    abilities = AbilityScores(
        strength=10,
        dexterity=10,
        constitution=10,
        intelligence=10,
        wisdom=10,
        charisma=10,
    )

    with pytest.raises(
        ValueError,
        match="name must not be blank",
    ):
        Character(
            name=invalid_name,
            level=1,
            character_class="Paladin",
            abilities=abilities,
        )


@pytest.mark.parametrize("invalid_class", ["", "   "])
def test_character_rejects_blank_class(
    invalid_class: str,
) -> None:
    abilities = AbilityScores(
        strength=10,
        dexterity=10,
        constitution=10,
        intelligence=10,
        wisdom=10,
        charisma=10,
    )

    with pytest.raises(
        ValueError,
        match="character_class must not be blank",
    ):
        Character(
            name="Arthur",
            level=1,
            character_class=invalid_class,
            abilities=abilities,
        )

    