from dataclasses import dataclass

from app.domain.character.calculations import ability_modifier


ABILITY_NAMES = (
    "strength",
    "dexterity",
    "constitution",
    "intelligence",
    "wisdom",
    "charisma",
)


@dataclass(frozen=True)
class AbilityScores:
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

    def __post_init__(self) -> None:
        for field in ABILITY_NAMES:
            score = getattr(self, field)

            if not 1 <= score <= 20:
                raise ValueError(
                    f"{field} must be between 1 and 20"
                )

    def modifier_for(self, ability: str) -> int:
        if ability not in ABILITY_NAMES:
            raise ValueError(f"unknown ability: {ability}")

        score = getattr(self, ability)

        return ability_modifier(score)