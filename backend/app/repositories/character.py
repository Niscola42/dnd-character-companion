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
        model = CharacterModel(owner_id=owner_id)
        self._apply_character(model, character)

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
        model = self._get_model(
            character_id=character_id,
            owner_id=owner_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def update_by_id_and_owner(
        self,
        character_id: int,
        owner_id: int,
        character: Character,
    ) -> Optional[Character]:
        model = self._get_model(
            character_id=character_id,
            owner_id=owner_id,
        )

        if model is None:
            return None

        self._apply_character(model, character)
        self._session.flush()

        return self._to_domain(model)

    def delete_by_id_and_owner(
        self,
        character_id: int,
        owner_id: int,
    ) -> bool:
        model = self._get_model(
            character_id=character_id,
            owner_id=owner_id,
        )

        if model is None:
            return False

        self._session.delete(model)
        self._session.flush()

        return True

    def _get_model(
        self,
        character_id: int,
        owner_id: int,
    ) -> Optional[CharacterModel]:
        statement = select(CharacterModel).where(
            CharacterModel.id == character_id,
            CharacterModel.owner_id == owner_id,
        )

        return self._session.scalar(statement)

    @staticmethod
    def _apply_character(
        model: CharacterModel,
        character: Character,
    ) -> None:
        model.name = character.name
        model.level = character.level
        model.character_class = (
            character.character_class
        )
        model.strength = character.abilities.strength
        model.dexterity = character.abilities.dexterity
        model.constitution = (
            character.abilities.constitution
        )
        model.intelligence = (
            character.abilities.intelligence
        )
        model.wisdom = character.abilities.wisdom
        model.charisma = character.abilities.charisma
        model.saving_throw_proficiencies = sorted(
            character.saving_throw_proficiencies
        )
        model.skill_proficiencies = sorted(
            character.skill_proficiencies
        )
        model.spellcasting_ability = (
            character.spellcasting_ability
        )

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