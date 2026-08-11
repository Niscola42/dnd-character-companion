from dataclasses import dataclass
from enum import Enum
from typing import Optional

from app.domain.character.health import HitPoints

from app.domain.resource.resource import (
    RecoveryType,
    Resource,
)


class RestType(str, Enum):
    SHORT = "SHORT"
    LONG = "LONG"


@dataclass(frozen=True)
class ResourceChange:
    name: str
    before: int
    after: int

@dataclass(frozen=True)
class HitPointChange:
    current_before: int
    current_after: int
    temporary_before: int
    temporary_after: int


@dataclass(frozen=True)
class RestSummary:
    changes: list[ResourceChange]
    hit_points: Optional[HitPointChange] = None


class RestEngine:
    @staticmethod
    def perform(
        rest_type: RestType,
        resources: list[Resource],
        hit_points: Optional[HitPoints] = None,
    ) -> RestSummary:
        changes: list[ResourceChange] = []

        for resource in resources:
            if not RestEngine._recovers_on_rest(
                resource.recovery_type,
                rest_type,
            ):
                continue

            before = resource.current
            resource.restore_full()

            if resource.current != before:
                changes.append(
                    ResourceChange(
                        name=resource.name,
                        before=before,
                        after=resource.current,
                    )
                )

        hit_point_change = None

        if (
            rest_type == RestType.LONG
            and hit_points is not None
        ):
            current_before = hit_points.current
            temporary_before = hit_points.temporary

            hit_points.restore_full()
            hit_points.clear_temporary_hp()

            if (
                hit_points.current != current_before
                or hit_points.temporary
                != temporary_before
            ):
                hit_point_change = HitPointChange(
                    current_before=current_before,
                    current_after=hit_points.current,
                    temporary_before=temporary_before,
                    temporary_after=(
                        hit_points.temporary
                    ),
                )

        return RestSummary(
            changes=changes,
            hit_points=hit_point_change,
        )

    @staticmethod
    def _recovers_on_rest(
        recovery_type: RecoveryType,
        rest_type: RestType,
    ) -> bool:
        if rest_type == RestType.SHORT:
            return (
                recovery_type
                == RecoveryType.SHORT_REST
            )

        return recovery_type in {
            RecoveryType.SHORT_REST,
            RecoveryType.LONG_REST,
        }