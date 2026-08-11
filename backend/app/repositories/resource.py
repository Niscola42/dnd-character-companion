from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.character import CharacterModel
from app.database.models.resource import ResourceModel
from app.domain.resource.resource import (
    RecoveryType,
    Resource,
)


class ResourceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(
        self,
        character_id: int,
        owner_id: int,
        resource: Resource,
    ) -> Optional[Resource]:
        if not self._character_is_owned(
            character_id=character_id,
            owner_id=owner_id,
        ):
            return None

        model = ResourceModel(
            character_id=character_id,
            name=resource.name,
            source=resource.source,
            maximum=resource.maximum,
            current=resource.current,
            recovery_type=resource.recovery_type.value,
            resource_metadata=resource.metadata,
        )

        self._session.add(model)
        self._session.flush()

        return self._to_domain(model)

    def list_by_character(
        self,
        character_id: int,
        owner_id: int,
    ) -> list[Resource]:
        statement = (
            select(ResourceModel)
            .join(
                CharacterModel,
                ResourceModel.character_id
                == CharacterModel.id,
            )
            .where(
                ResourceModel.character_id
                == character_id,
                CharacterModel.owner_id == owner_id,
            )
            .order_by(ResourceModel.id)
        )

        models = self._session.scalars(statement).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def get_by_id_and_owner(
        self,
        resource_id: int,
        owner_id: int,
    ) -> Optional[Resource]:
        model = self._get_model(
            resource_id=resource_id,
            owner_id=owner_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def update_by_id_and_owner(
        self,
        resource_id: int,
        owner_id: int,
        resource: Resource,
    ) -> Optional[Resource]:
        model = self._get_model(
            resource_id=resource_id,
            owner_id=owner_id,
        )

        if model is None:
            return None

        self._apply_resource(model, resource)
        self._session.flush()

        return self._to_domain(model)

    def delete_by_id_and_owner(
        self,
        resource_id: int,
        owner_id: int,
    ) -> bool:
        model = self._get_model(
            resource_id=resource_id,
            owner_id=owner_id,
        )

        if model is None:
            return False

        self._session.delete(model)
        self._session.flush()

        return True

    def _get_model(
        self,
        resource_id: int,
        owner_id: int,
    ) -> Optional[ResourceModel]:
        statement = (
            select(ResourceModel)
            .join(
                CharacterModel,
                ResourceModel.character_id
                == CharacterModel.id,
            )
            .where(
                ResourceModel.id == resource_id,
                CharacterModel.owner_id == owner_id,
            )
        )

        return self._session.scalar(statement)

    @staticmethod
    def _apply_resource(
        model: ResourceModel,
        resource: Resource,
    ) -> None:
        model.name = resource.name
        model.source = resource.source
        model.maximum = resource.maximum
        model.current = resource.current
        model.recovery_type = (
            resource.recovery_type.value
        )
        model.resource_metadata = resource.metadata

    def _character_is_owned(
        self,
        character_id: int,
        owner_id: int,
    ) -> bool:
        statement = select(CharacterModel.id).where(
            CharacterModel.id == character_id,
            CharacterModel.owner_id == owner_id,
        )

        return self._session.scalar(statement) is not None

    @staticmethod
    def _to_domain(
        model: ResourceModel,
    ) -> Resource:
        return Resource(
            id=model.id,
            character_id=model.character_id,
            name=model.name,
            source=model.source,
            maximum=model.maximum,
            current=model.current,
            recovery_type=RecoveryType(
                model.recovery_type
            ),
            metadata=model.resource_metadata,
        )