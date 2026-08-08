import pytest
from app.domain.character.abilities import AbilityScores


def test_ability_scores_store_all_six_scores() -> None:
    scores = AbilityScores(
        strength=16,
        dexterity=12,
        constitution=14,
        intelligence=8,
        wisdom=10,
        charisma=18,
    )

    assert scores.strength == 16
    assert scores.dexterity == 12
    assert scores.constitution == 14
    assert scores.intelligence == 8
    assert scores.wisdom == 10
    assert scores.charisma == 18

@pytest.mark.parametrize(
    "field",
    [
        "strength",
        "dexterity",
        "constitution",
        "intelligence",
        "wisdom",
        "charisma",
    ],
)
@pytest.mark.parametrize("invalid_score", [0, 21])
def test_ability_scores_reject_invalid_scores(
    field: str,
    invalid_score: int,
) -> None:
    scores = {
        "strength": 10,
        "dexterity": 10,
        "constitution": 10,
        "intelligence": 10,
        "wisdom": 10,
        "charisma": 10,
    }
    scores[field] = invalid_score

    with pytest.raises(
        ValueError,
        match=f"{field} must be between 1 and 20",
    ):
        AbilityScores(**scores)

@pytest.mark.parametrize(
    ("ability", "expected_modifier"),
    [
        ("strength", 3),
        ("dexterity", 1),
        ("constitution", 2),
        ("intelligence", -1),
        ("wisdom", 0),
        ("charisma", 4),
    ],
)
def test_ability_scores_calculate_modifiers(
    ability: str,
    expected_modifier: int,
) -> None:
    scores = AbilityScores(
        strength=16,
        dexterity=12,
        constitution=14,
        intelligence=8,
        wisdom=10,
        charisma=18,
    )

    assert scores.modifier_for(ability) == expected_modifier

def test_ability_scores_reject_unknown_ability() -> None:
    scores = AbilityScores(
        strength=10,
        dexterity=10,
        constitution=10,
        intelligence=10,
        wisdom=10,
        charisma=10,
    )

    with pytest.raises(
        ValueError,
        match="unknown ability: luck",
    ):
        scores.modifier_for("luck")