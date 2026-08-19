from typing import Optional

from pydantic import BaseModel, Field


class AbilityScoresRequest(BaseModel):
    strength: int = Field(ge=1, le=20)
    dexterity: int = Field(ge=1, le=20)
    constitution: int = Field(ge=1, le=20)
    intelligence: int = Field(ge=1, le=20)
    wisdom: int = Field(ge=1, le=20)
    charisma: int = Field(ge=1, le=20)

class HitPointsRequest(BaseModel):
    maximum: int = Field(gt=0)
    current: int = Field(ge=0)
    temporary: int = Field(default=0, ge=0)


class CharacterCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    level: int = Field(ge=1, le=5)
    hit_points: HitPointsRequest
    character_class: str = Field(
        min_length=1,
        max_length=50,
    )
    species: str = Field(
        min_length=1,
        max_length=50,
    )
    background: str = Field(
        min_length=1,
        max_length=100,
    )
    abilities: AbilityScoresRequest
    saving_throw_proficiencies: set[str] = Field(
        default_factory=set
    )
    skill_proficiencies: set[str] = Field(
        default_factory=set
    )
    spellcasting_ability: Optional[str] = None



class CharacterResponse(BaseModel):
    id: int
    name: str
    level: int
    character_class: str
    portrait_url: Optional[str] = None
    species: Optional[str] = None
    background: Optional[str] = None
    abilities: AbilityScoresRequest
    hit_points: HitPointsRequest
    saving_throw_proficiencies: list[str]
    skill_proficiencies: list[str]
    spellcasting_ability: Optional[str]

    ability_modifiers: dict[str, int]
    saving_throw_modifiers: dict[str, int]
    skill_modifiers: dict[str, int]

    proficiency_bonus: int
    initiative: int
    passive_perception: int
    spell_attack_modifier: Optional[int]
    spell_save_dc: Optional[int]

class HitPointActionRequest(BaseModel):
    amount: int = Field(ge=0)