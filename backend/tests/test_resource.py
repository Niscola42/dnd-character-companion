import pytest

from app.domain.resource.resource import (
    InsufficientResourceError,
    RecoveryType,
    Resource,
)


def test_resource_can_be_consumed_and_restored() -> None:
    resource = Resource(
        name="Channel Divinity",
        maximum=2,
        current=2,
        recovery_type=RecoveryType.SHORT_REST,
    )

    resource.consume(1)

    assert resource.current == 1

    resource.restore(5)

    assert resource.current == 2


def test_resource_rejects_consumption_above_current() -> None:
    resource = Resource(
        name="Channel Divinity",
        maximum=2,
        current=1,
        recovery_type=RecoveryType.SHORT_REST,
    )

    with pytest.raises(InsufficientResourceError):
        resource.consume(2)

    assert resource.current == 1

def test_resource_can_be_fully_restored() -> None:
    resource = Resource(
        name="Lay on Hands",
        maximum=25,
        current=8,
        recovery_type=RecoveryType.LONG_REST,
    )

    resource.restore_full()

    assert resource.current == 25


def test_resource_rejects_invalid_initial_state() -> None:
    with pytest.raises(
        ValueError,
        match="resource name must not be blank",
    ):
        Resource(
            name="   ",
            maximum=1,
            current=1,
            recovery_type=RecoveryType.MANUAL,
        )

    with pytest.raises(
        ValueError,
        match="resource maximum must be positive",
    ):
        Resource(
            name="Test",
            maximum=0,
            current=0,
            recovery_type=RecoveryType.MANUAL,
        )

    with pytest.raises(
        ValueError,
        match="resource current must be between 0 and maximum",
    ):
        Resource(
            name="Test",
            maximum=2,
            current=3,
            recovery_type=RecoveryType.MANUAL,
        )


@pytest.mark.parametrize(
    "operation",
    ["consume", "restore"],
)
def test_resource_rejects_negative_amounts(
    operation: str,
) -> None:
    resource = Resource(
        name="Test",
        maximum=2,
        current=1,
        recovery_type=RecoveryType.MANUAL,
    )

    with pytest.raises(
        ValueError,
        match="amount must not be negative",
    ):
        getattr(resource, operation)(-1)