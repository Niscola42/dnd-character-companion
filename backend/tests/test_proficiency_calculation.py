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