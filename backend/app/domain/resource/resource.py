from dataclasses import dataclass
from enum import Enum


class RecoveryType(str, Enum):
    SHORT_REST = "SHORT_REST"
    LONG_REST = "LONG_REST"
    MANUAL = "MANUAL"


class InsufficientResourceError(Exception):
    pass


@dataclass
class Resource:
    name: str
    maximum: int
    current: int
    recovery_type: RecoveryType

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError(
                "resource name must not be blank"
            )

        if self.maximum <= 0:
            raise ValueError(
                "resource maximum must be positive"
            )

        if not 0 <= self.current <= self.maximum:
            raise ValueError(
                "resource current must be between 0 and maximum"
            )

    @staticmethod
    def _validate_amount(amount: int) -> None:
        if amount < 0:
            raise ValueError(
                "amount must not be negative"
            )

    def consume(self, amount: int) -> None:
        self._validate_amount(amount)
        if amount > self.current:
            raise InsufficientResourceError

        self.current -= amount

    def restore(self, amount: int) -> None:
        self._validate_amount(amount)
        self.current = min(
            self.maximum,
            self.current + amount,
        )

    def restore_full(self) -> None:
        self.current = self.maximum
