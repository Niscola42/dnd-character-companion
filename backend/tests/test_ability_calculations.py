import pytest

from app.domain.character.calculations import ability_modifier


@pytest.mark.parametrize(
    ("score", "expected_modifier"),
    [
        (1, -5),
        (8, -1),
        (9, -1),
        (10, 0),
        (11, 0),
        (18, 4),
        (20, 5),
    ],
)
def test_ability_modifier(
    score: int,
    expected_modifier: int,
) -> None:
    assert ability_modifier(score) == expected_modifier