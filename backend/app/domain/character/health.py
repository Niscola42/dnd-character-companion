from dataclasses import dataclass


@dataclass
class HitPoints:
    maximum: int
    current: int
    temporary: int = 0

    def take_damage(self, amount: int) -> None:
        self._validate_amount(amount)
        absorbed = min(self.temporary, amount)

        self.temporary -= absorbed
        remaining_damage = amount - absorbed
        self.current = max(
            0,
            self.current - remaining_damage,
        )

    def heal(self, amount: int) -> None:
        self._validate_amount(amount)
        self.current = min(
            self.maximum,
            self.current + amount,
        )

    def add_temporary_hp(self, amount: int) -> None:
        self._validate_amount(amount)
        self.temporary = max(
            self.temporary,
            amount,
        )
    def __post_init__(self) -> None:
        if self.maximum <= 0:
            raise ValueError(
                "maximum HP must be positive"
            )

        if not 0 <= self.current <= self.maximum:
            raise ValueError(
                "current HP must be between 0 and maximum"
            )

        if self.temporary < 0:
            raise ValueError(
                "temporary HP must not be negative"
            )

    @staticmethod
    def _validate_amount(amount: int) -> None:
        if amount < 0:
            raise ValueError(
                "amount must not be negative"
            )

    def restore_full(self) -> None:
        self.current = self.maximum

    def clear_temporary_hp(self) -> None:
        self.temporary = 0