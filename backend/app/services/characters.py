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

    def update_for_owner(
        self,
        character_id: int,
        owner_id: int,
        character: Character,
    ) -> Character:
        updated = (
            self._repository.update_by_id_and_owner(
                character_id=character_id,
                owner_id=owner_id,
                character=character,
            )
        )

        if updated is None:
            raise CharacterNotFoundError

        return updated

    def change_hit_points(
        self,
        character_id: int,
        owner_id: int,
        action: str,
        amount: int,
    ) -> Character:
        character = self.get_for_owner(
            character_id=character_id,
            owner_id=owner_id,
        )

        actions = {
            "damage": character.hit_points.take_damage,
            "heal": character.hit_points.heal,
            "temporary": (
                character.hit_points.add_temporary_hp
            ),
        }

        try:
            operation = actions[action]
        except KeyError as error:
            raise ValueError(
                "unknown hit point action"
            ) from error

        operation(amount)

        return self.update_for_owner(
            character_id=character_id,
            owner_id=owner_id,
            character=character,
        )

    def delete_for_owner(
        self,
        character_id: int,
        owner_id: int,
    ) -> None:
        deleted = (
            self._repository.delete_by_id_and_owner(
                character_id=character_id,
                owner_id=owner_id,
            )
        )

        if not deleted:
            raise CharacterNotFoundError