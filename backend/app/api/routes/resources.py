from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.database.connection import get_db_session
from app.database.models.user import UserModel
from app.domain.resource.resource import (
    InsufficientResourceError,
    Resource,
)
from app.repositories.resource import ResourceRepository
from app.schemas.resource import (
    ResourceAmountRequest,
    ResourceCreateRequest,
    ResourceResponse,
)


router = APIRouter(
    prefix="/characters/{character_id}/resources",
    tags=["Resources"],
)


def to_response(resource: Resource) -> ResourceResponse:
    if (
        resource.id is None
        or resource.character_id is None
    ):
        raise RuntimeError(
            "persisted resource must have ids"
        )

    return ResourceResponse(
        id=resource.id,
        character_id=resource.character_id,
        name=resource.name,
        source=resource.source,
        maximum=resource.maximum,
        current=resource.current,
        recovery_type=resource.recovery_type,
        metadata=resource.metadata,
    )


@router.post(
    "",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_resource(
    character_id: int,
    payload: ResourceCreateRequest,
    user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> ResourceResponse:
    try:
        resource = Resource(
            name=payload.name,
            source=payload.source,
            maximum=payload.maximum,
            current=payload.current,
            recovery_type=payload.recovery_type,
            metadata=payload.metadata,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(error),
        ) from error

    created = ResourceRepository(session).add(
        character_id=character_id,
        owner_id=user.id,
        resource=resource,
    )

    if created is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="character not found",
        )

    return to_response(created)


@router.get(
    "",
    response_model=list[ResourceResponse],
)
def list_resources(
    character_id: int,
    user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> list[ResourceResponse]:
    resources = ResourceRepository(
        session
    ).list_by_character(
        character_id=character_id,
        owner_id=user.id,
    )

    return [
        to_response(resource)
        for resource in resources
    ]

def change_resource_amount(
    character_id: int,
    resource_id: int,
    owner_id: int,
    amount: int,
    action: str,
    session: Session,
) -> Resource:
    repository = ResourceRepository(session)

    resource = repository.get_by_id_and_owner(
        resource_id=resource_id,
        owner_id=owner_id,
    )

    if (
        resource is None
        or resource.character_id != character_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="resource not found",
        )

    try:
        if action == "consume":
            resource.consume(amount)
        else:
            resource.restore(amount)
    except InsufficientResourceError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="insufficient resource",
        ) from error
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(error),
        ) from error

    updated = repository.update_by_id_and_owner(
        resource_id=resource_id,
        owner_id=owner_id,
        resource=resource,
    )

    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="resource not found",
        )

    return updated

@router.post(
    "/{resource_id}/consume",
    response_model=ResourceResponse,
)
def consume_resource(
    character_id: int,
    resource_id: int,
    payload: ResourceAmountRequest,
    user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> ResourceResponse:
    resource = change_resource_amount(
        character_id=character_id,
        resource_id=resource_id,
        owner_id=user.id,
        amount=payload.amount,
        action="consume",
        session=session,
    )

    return to_response(resource)


@router.post(
    "/{resource_id}/restore",
    response_model=ResourceResponse,
)
def restore_resource(
    character_id: int,
    resource_id: int,
    payload: ResourceAmountRequest,
    user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> ResourceResponse:
    resource = change_resource_amount(
        character_id=character_id,
        resource_id=resource_id,
        owner_id=user.id,
        amount=payload.amount,
        action="restore",
        session=session,
    )

    return to_response(resource)