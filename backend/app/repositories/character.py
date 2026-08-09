from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.character import CharacterModel
from app.domain.character.abilities import AbilityScores
from app.domain.character.character import Character


class CharacterRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(
        self,
        owner_id: int,
        character: Character,
    ) -> Character:
        model = CharacterModel(
            owner_id=owner_id,
            name=character.name,
            level=character.level,
            character_class=character.character_class,
            strength=character.abilities.strength,
            dexterity=character.abilities.dexterity,
            constitution=character.abilities.constitution,
            intelligence=character.abilities.intelligence,
            wisdom=character.abilities.wisdom,
            charisma=character.abilities.charisma,
            saving_throw_proficiencies=sorted(
                character.saving_throw_proficiencies
            ),
            skill_proficiencies=sorted(
                character.skill_proficiencies
            ),
            spellcasting_ability=(
                character.spellcasting_ability
            ),
        )

        self._session.add(model)
        self._session.flush()

        return self._to_domain(model)

    def list_by_owner(
        self,
        owner_id: int,
    ) -> list[Character]:
        statement = (
            select(CharacterModel)
            .where(CharacterModel.owner_id == owner_id)
            .order_by(CharacterModel.id)
        )
        models = self._session.scalars(statement).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def get_by_id_and_owner(
        self,
        character_id: int,
        owner_id: int,
    ) -> Optional[Character]:
        statement = select(CharacterModel).where(
            CharacterModel.id == character_id,
            CharacterModel.owner_id == owner_id,
        )
        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model)

    @staticmethod
    def _to_domain(model: CharacterModel) -> Character:
        return Character(
            id=model.id,
            owner_id=model.owner_id,
            name=model.name,
            level=model.level,
            character_class=model.character_class,
            abilities=AbilityScores(
                strength=model.strength,
                dexterity=model.dexterity,
                constitution=model.constitution,
                intelligence=model.intelligence,
                wisdom=model.wisdom,
                charisma=model.charisma,
            ),
            saving_throw_proficiencies=frozenset(
                model.saving_throw_proficiencies
            ),
            skill_proficiencies=frozenset(
                model.skill_proficiencies
            ),
            spellcasting_ability=(
                model.spellcasting_ability
            ),
        )