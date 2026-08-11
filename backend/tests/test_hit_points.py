from app.domain.character.health import HitPoints

import pytest

def test_damage_consumes_temporary_hp_first() -> None:
    hit_points = HitPoints(
        maximum=30,
        current=20,
        temporary=8,
    )

    hit_points.take_damage(10)

    assert hit_points.temporary == 0
    assert hit_points.current == 18


def test_damage_never_reduces_current_hp_below_zero() -> None:
    hit_points = HitPoints(
        maximum=30,
        current=5,
    )

    hit_points.take_damage(20)

    assert hit_points.temporary == 0
    assert hit_points.current == 0

def test_healing_restores_hp_up_to_maximum() -> None:
    hit_points = HitPoints(
        maximum=30,
        current=10,
    )

    hit_points.heal(25)

    assert hit_points.current == 30


def test_temporary_hp_keeps_only_the_higher_value() -> None:
    hit_points = HitPoints(
        maximum=30,
        current=20,
        temporary=5,
    )

    hit_points.add_temporary_hp(3)

    assert hit_points.temporary == 5

    hit_points.add_temporary_hp(8)

    assert hit_points.temporary == 8

def test_hit_points_reject_invalid_initial_state() -> None:
    with pytest.raises(
        ValueError,
        match="maximum HP must be positive",
    ):
        HitPoints(maximum=0, current=0)

    with pytest.raises(
        ValueError,
        match="current HP must be between 0 and maximum",
    ):
        HitPoints(maximum=30, current=-1)

    with pytest.raises(
        ValueError,
        match="current HP must be between 0 and maximum",
    ):
        HitPoints(maximum=30, current=31)

    with pytest.raises(
        ValueError,
        match="temporary HP must not be negative",
    ):
        HitPoints(
            maximum=30,
            current=20,
            temporary=-1,
        )


@pytest.mark.parametrize(
    "operation",
    [
        "take_damage",
        "heal",
        "add_temporary_hp",
    ],
)
def test_hit_point_operations_reject_negative_amounts(
    operation: str,
) -> None:
    hit_points = HitPoints(
        maximum=30,
        current=20,
    )

    with pytest.raises(
        ValueError,
        match="amount must not be negative",
    ):
        getattr(hit_points, operation)(-1)