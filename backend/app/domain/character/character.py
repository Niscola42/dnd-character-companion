from dataclasses import dataclass

from app.domain.character.abilities import AbilityScores

from app.domain.character.calculations import (
    proficiency_bonus as calculate_proficiency_bonus,
)

@dataclass
class Character:
    name: str
    level: int
    character_class: str
    abilities: AbilityScores

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name must not be blank")

        if not self.character_class.strip():
            raise ValueError("character_class must not be blank")

        if not 1 <= self.level <= 5:
            raise ValueError("level must be between 1 and 5")

    @property
    def proficiency_bonus(self) -> int:
        return calculate_proficiency_bonus(self.level)

    @property
    def initiative(self) -> int:
        return self.abilities.modifier_for("dexterity")