from app.domain.resource.resource import (
    RecoveryType,
    Resource,
)
from app.domain.resource.rest import (
    HitPointChange,
    ResourceChange,
    RestEngine,
    RestType,
)
from app.domain.character.health import HitPoints


def test_short_rest_restores_only_short_rest_resources() -> None:
    channel_divinity = Resource(
        name="Channel Divinity",
        maximum=2,
        current=0,
        recovery_type=RecoveryType.SHORT_REST,
    )
    lay_on_hands = Resource(
        name="Lay on Hands",
        maximum=25,
        current=8,
        recovery_type=RecoveryType.LONG_REST,
    )
    manual_resource = Resource(
        name="Manual Resource",
        maximum=3,
        current=1,
        recovery_type=RecoveryType.MANUAL,
    )

    summary = RestEngine.perform(
        rest_type=RestType.SHORT,
        resources=[
            channel_divinity,
            lay_on_hands,
            manual_resource,
        ],
    )

    assert channel_divinity.current == 2
    assert lay_on_hands.current == 8
    assert manual_resource.current == 1
    assert summary.changes == [
        ResourceChange(
            name="Channel Divinity",
            before=0,
            after=2,
        )
    ]


def test_long_rest_restores_short_and_long_rest_resources() -> None:
    channel_divinity = Resource(
        name="Channel Divinity",
        maximum=2,
        current=0,
        recovery_type=RecoveryType.SHORT_REST,
    )
    lay_on_hands = Resource(
        name="Lay on Hands",
        maximum=25,
        current=8,
        recovery_type=RecoveryType.LONG_REST,
    )

    summary = RestEngine.perform(
        rest_type=RestType.LONG,
        resources=[
            channel_divinity,
            lay_on_hands,
        ],
    )

    assert channel_divinity.current == 2
    assert lay_on_hands.current == 25
    assert summary.changes == [
        ResourceChange(
            name="Channel Divinity",
            before=0,
            after=2,
        ),
        ResourceChange(
            name="Lay on Hands",
            before=8,
            after=25,
        ),
    ]

def test_long_rest_restores_hp_and_removes_temporary_hp() -> None:
    hit_points = HitPoints(
        maximum=30,
        current=12,
        temporary=4,
    )

    summary = RestEngine.perform(
        rest_type=RestType.LONG,
        resources=[],
        hit_points=hit_points,
    )

    assert hit_points.current == 30
    assert hit_points.temporary == 0
    assert summary.hit_points == HitPointChange(
        current_before=12,
        current_after=30,
        temporary_before=4,
        temporary_after=0,
    )


def test_short_rest_does_not_automatically_change_hp() -> None:
    hit_points = HitPoints(
        maximum=30,
        current=12,
        temporary=4,
    )

    summary = RestEngine.perform(
        rest_type=RestType.SHORT,
        resources=[],
        hit_points=hit_points,
    )

    assert hit_points.current == 12
    assert hit_points.temporary == 4
    assert summary.hit_points is None