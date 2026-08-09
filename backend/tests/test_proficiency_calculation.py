import pytest

from app.domain.character.calculations import proficiency_bonus


@pytest.mark.parametrize(
    ("level", "expected_bonus"),
    [
        (1, 2),
        (4, 2),
        (5, 3),
        (8, 3),
        (9, 4),
        (12, 4),
        (13, 5),
        (16, 5),
        (17, 6),
        (20, 6),
    ],
)
def test_proficiency_bonus(
    level: int,
    expected_bonus: int,
) -> None:
    assert proficiency_bonus(level) == expected_bonus

@pytest.mark.parametrize("invalid_level", [0, -1, 21])
def test_proficiency_bonus_rejects_invalid_level(
    invalid_level: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="level must be between 1 and 20",
    ):
        proficiency_bonus(invalid_level)

