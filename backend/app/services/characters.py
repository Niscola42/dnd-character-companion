from app.domain.character.character import Character
from app.repositories.character import CharacterRepository


class CharacterNotFoundError(Exception):
    pass


class CharacterService:
    def __init__(
        self,
        repository: CharacterRepository,
    ) -> None:
        self._repository = repository

    def create(
        self,
        owner_id: int,
        character: Character,
    ) -> Character:
        return self._repository.add(
            owner_id=owner_id,
            character=character,
        )

    def list_for_owner(
        self,
        owner_id: int,
    ) -> list[Character]:
        return self._repository.list_by_owner(owner_id)

    def get_for_owner(
        self,
        character_id: int,
        owner_id: int,
    ) -> Character:
        character = (
            self._repository.get_by_id_and_owner(
                character_id=character_id,
                owner_id=owner_id,
            )
        )

        if character is None:
            raise CharacterNotFoundError

        return character