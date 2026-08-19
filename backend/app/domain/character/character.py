from dataclasses import dataclass, field
from typing import Optional

from app.domain.character.skills import SKILL_ABILITIES
from app.domain.character.health import HitPoints


from app.domain.character.abilities import (
    ABILITY_NAMES,
    AbilityScores,
)

from app.domain.character.calculations import (
    proficiency_bonus as calculate_proficiency_bonus,
)

@dataclass
class Character:
    name: str
    level: int
    character_class: str
    abilities: AbilityScores
    hit_points: HitPoints = field(
        default_factory=lambda: HitPoints(
            maximum=1,
            current=1,
        )
    )
    saving_throw_proficiencies: frozenset[str] = field(
    default_factory=frozenset
    )
    skill_proficiencies: frozenset[str] = field(
        default_factory=frozenset
    )
    spellcasting_ability: Optional[str] = None
    id: Optional[int] = None
    owner_id: Optional[int] = None
    portrait_url: Optional[str] = None
    species: Optional[str] = None
    background: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name must not be blank")

        if not self.character_class.strip():
            raise ValueError(
                "character_class must not be blank"
            )

        if (
            self.species is not None
            and not self.species.strip()
        ):
            raise ValueError("species must not be blank")

        if (
            self.background is not None
            and not self.background.strip()
        ):
            raise ValueError(
                "background must not be blank"
            )

        if not 1 <= self.level <= 5:
            raise ValueError(
                "level must be between 1 and 5"
            )

        for ability in self.saving_throw_proficiencies:
            if ability not in ABILITY_NAMES:
                raise ValueError(
                    "unknown saving throw proficiency: "
                    f"{ability}"
                )

        for skill in self.skill_proficiencies:
            if skill not in SKILL_ABILITIES:
                raise ValueError(
                    f"unknown skill proficiency: {skill}"
                )

        if (
            self.spellcasting_ability is not None
            and self.spellcasting_ability not in ABILITY_NAMES
        ):
            raise ValueError(
                "unknown spellcasting ability: "
                f"{self.spellcasting_ability}"
            )

    @property
    def proficiency_bonus(self) -> int:
        return calculate_proficiency_bonus(self.level)

    @property
    def initiative(self) -> int:
        return self.abilities.modifier_for("dexterity")
    
    @property
    def passive_perception(self) -> int:
        return 10 + self.skill_modifier("perception")

    def saving_throw_modifier(self, ability: str) -> int:
        modifier = self.abilities.modifier_for(ability)

        if ability in self.saving_throw_proficiencies:
            modifier += self.proficiency_bonus

        return modifier
    
    def skill_modifier(self, skill: str) -> int:
        if skill not in SKILL_ABILITIES:
            raise ValueError(f"unknown skill: {skill}")

        ability = SKILL_ABILITIES[skill]
        modifier = self.abilities.modifier_for(ability)

        if skill in self.skill_proficiencies:
            modifier += self.proficiency_bonus

        return modifier

    def _spellcasting_modifier(self) -> int:
        if self.spellcasting_ability is None:
            raise ValueError(
                "character has no spellcasting ability"
            )

        return self.abilities.modifier_for(
            self.spellcasting_ability
        )

    @property
    def spell_attack_modifier(self) -> int:
        return (
            self._spellcasting_modifier()
            + self.proficiency_bonus
        )

    @property
    def spell_save_dc(self) -> int:
        return (
            8
            + self._spellcasting_modifier()
            + self.proficiency_bonus
        )
    