from dataclasses import dataclass


@dataclass(frozen=True)
class AbilityScores:
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

    def __post_init__(self) -> None:
        fields = (
            "strength",
            "dexterity",
            "constitution",
            "intelligence",
            "wisdom",
            "charisma",
        )

        for field in fields:
            score = getattr(self, field)

            if not 1 <= score <= 20:
                raise ValueError(
                    f"{field} must be between 1 and 20"
                )