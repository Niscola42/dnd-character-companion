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