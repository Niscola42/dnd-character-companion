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

def test_character_calculates_proficiency_bonus() -> None:
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

    assert character.proficiency_bonus == 3

def test_character_calculates_initiative() -> None:
    abilities = AbilityScores(
        strength=16,
        dexterity=14,
        constitution=12,
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

    assert character.initiative == 2

def test_character_calculates_saving_throw_modifiers() -> None:
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
        saving_throw_proficiencies=frozenset(
            {"wisdom", "charisma"}
        ),
    )

    assert character.saving_throw_modifier("strength") == 3
    assert character.saving_throw_modifier("wisdom") == 3
    assert character.saving_throw_modifier("charisma") == 7

def test_character_rejects_unknown_saving_throw_proficiency() -> None:
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
        match="unknown saving throw proficiency: luck",
    ):
        Character(
            name="Arthur",
            level=1,
            character_class="Paladin",
            abilities=abilities,
            saving_throw_proficiencies=frozenset({"luck"}),
        )

def test_character_calculates_skill_modifiers() -> None:
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
        skill_proficiencies=frozenset(
            {"athletics", "persuasion"}
        ),
    )

    assert character.skill_modifier("athletics") == 6
    assert character.skill_modifier("stealth") == 1
    assert character.skill_modifier("persuasion") == 7

def test_character_rejects_unknown_skill_proficiency() -> None:
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
        match="unknown skill proficiency: luck",
    ):
        Character(
            name="Arthur",
            level=1,
            character_class="Paladin",
            abilities=abilities,
            skill_proficiencies=frozenset({"luck"}),
        )


def test_character_rejects_unknown_skill_query() -> None:
    abilities = AbilityScores(
        strength=10,
        dexterity=10,
        constitution=10,
        intelligence=10,
        wisdom=10,
        charisma=10,
    )

    character = Character(
        name="Arthur",
        level=1,
        character_class="Paladin",
        abilities=abilities,
    )

    with pytest.raises(
        ValueError,
        match="unknown skill: luck",
    ):
        character.skill_modifier("luck")

def test_character_calculates_passive_perception() -> None:
    abilities = AbilityScores(
        strength=16,
        dexterity=12,
        constitution=14,
        intelligence=8,
        wisdom=14,
        charisma=18,
    )

    character = Character(
        name="Arthur",
        level=5,
        character_class="Paladin",
        abilities=abilities,
        skill_proficiencies=frozenset({"perception"}),
    )

    assert character.passive_perception == 15

def test_character_calculates_spellcasting_statistics() -> None:
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
        spellcasting_ability="charisma",
    )

    assert character.spell_attack_modifier == 7
    assert character.spell_save_dc == 15

def test_character_rejects_unknown_spellcasting_ability() -> None:
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
        match="unknown spellcasting ability: luck",
    ):
        Character(
            name="Arthur",
            level=1,
            character_class="Paladin",
            abilities=abilities,
            spellcasting_ability="luck",
        )


@pytest.mark.parametrize(
    "statistic",
    ["spell_attack_modifier", "spell_save_dc"],
)
def test_non_spellcaster_rejects_spellcasting_statistic(
    statistic: str,
) -> None:
    abilities = AbilityScores(
        strength=10,
        dexterity=10,
        constitution=10,
        intelligence=10,
        wisdom=10,
        charisma=10,
    )

    character = Character(
        name="Arthur",
        level=1,
        character_class="Fighter",
        abilities=abilities,
    )

    with pytest.raises(
        ValueError,
        match="character has no spellcasting ability",
    ):
        getattr(character, statistic)