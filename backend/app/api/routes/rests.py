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
from app.domain.resource.rest import RestEngine
from app.repositories.character import CharacterRepository
from app.repositories.resource import ResourceRepository
from app.schemas.rest import (
    HitPointChangeResponse,
    ResourceChangeResponse,
    RestRequest,
    RestResponse,
)


router = APIRouter(
    prefix="/characters/{character_id}/rests",
    tags=["Rests"],
)


@router.post(
    "",
    response_model=RestResponse,
)
def perform_rest(
    character_id: int,
    payload: RestRequest,
    user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> RestResponse:
    character_repository = CharacterRepository(session)
    resource_repository = ResourceRepository(session)

    character = (
        character_repository.get_by_id_and_owner(
            character_id=character_id,
            owner_id=user.id,
        )
    )

    if character is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="character not found",
        )

    resources = resource_repository.list_by_character(
        character_id=character_id,
        owner_id=user.id,
    )

    summary = RestEngine.perform(
        rest_type=payload.rest_type,
        resources=resources,
        hit_points=character.hit_points,
    )

    character_repository.update_by_id_and_owner(
        character_id=character_id,
        owner_id=user.id,
        character=character,
    )

    for resource in resources:
        if resource.id is None:
            raise RuntimeError(
                "persisted resource must have an id"
            )

        resource_repository.update_by_id_and_owner(
            resource_id=resource.id,
            owner_id=user.id,
            resource=resource,
        )

    hit_point_response = None

    if summary.hit_points is not None:
        hit_point_response = HitPointChangeResponse(
            current_before=(
                summary.hit_points.current_before
            ),
            current_after=(
                summary.hit_points.current_after
            ),
            temporary_before=(
                summary.hit_points.temporary_before
            ),
            temporary_after=(
                summary.hit_points.temporary_after
            ),
        )

    return RestResponse(
        changes=[
            ResourceChangeResponse(
                name=change.name,
                before=change.before,
                after=change.after,
            )
            for change in summary.changes
        ],
        hit_points=hit_point_response,
    )