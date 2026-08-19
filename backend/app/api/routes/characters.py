from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
    File,
    UploadFile,
)

from pathlib import Path
from uuid import uuid4

from app.config import settings
from sqlalchemy.orm import Session

from app.domain.character.health import HitPoints

from app.api.dependencies.auth import get_current_user
from app.database.connection import get_db_session
from app.database.models.user import UserModel
from app.domain.character.abilities import (
    ABILITY_NAMES,
    AbilityScores,
)
from app.domain.character.character import Character
from app.domain.character.skills import SKILL_ABILITIES
from app.repositories.character import CharacterRepository
from app.schemas.character import (
    AbilityScoresRequest,
    CharacterCreateRequest,
    CharacterResponse,
    HitPointsRequest,
    HitPointActionRequest,
)
from app.services.characters import (
    CharacterNotFoundError,
    CharacterService,
)


router = APIRouter(
    prefix="/characters",
    tags=["Characters"],
)

def from_request(
    payload: CharacterCreateRequest,
) -> Character:
    return Character(
        name=payload.name,
        level=payload.level,
        character_class=payload.character_class,
        species=payload.species,
        background=payload.background,
        abilities=AbilityScores(
            **payload.abilities.model_dump()
        ),
        saving_throw_proficiencies=frozenset(
            payload.saving_throw_proficiencies
        ),
        skill_proficiencies=frozenset(
            payload.skill_proficiencies
        ),
        spellcasting_ability=(
            payload.spellcasting_ability
        ),
        hit_points=HitPoints(
            maximum=payload.hit_points.maximum,
            current=payload.hit_points.current,
            temporary=payload.hit_points.temporary,
        ),
    )

def to_response(
    character: Character,
) -> CharacterResponse:
    if character.id is None:
        raise RuntimeError(
            "persisted character must have an id"
        )

    spell_attack_modifier = None
    spell_save_dc = None

    if character.spellcasting_ability is not None:
        spell_attack_modifier = (
            character.spell_attack_modifier
        )
        spell_save_dc = character.spell_save_dc

    return CharacterResponse(
        id=character.id,
        name=character.name,
        level=character.level,
        character_class=character.character_class,
        portrait_url=character.portrait_url,
        species=character.species,
        background=character.background,
        abilities=AbilityScoresRequest(
            strength=character.abilities.strength,
            dexterity=character.abilities.dexterity,
            constitution=character.abilities.constitution,
            intelligence=character.abilities.intelligence,
            wisdom=character.abilities.wisdom,
            charisma=character.abilities.charisma,
        ),
        hit_points=HitPointsRequest(
            maximum=character.hit_points.maximum,
            current=character.hit_points.current,
            temporary=character.hit_points.temporary,
        ),
        saving_throw_proficiencies=sorted(
            character.saving_throw_proficiencies
        ),
        skill_proficiencies=sorted(
            character.skill_proficiencies
        ),
        spellcasting_ability=(
            character.spellcasting_ability
        ),
        ability_modifiers={
            ability: character.abilities.modifier_for(
                ability
            )
            for ability in ABILITY_NAMES
        },
        saving_throw_modifiers={
            ability: character.saving_throw_modifier(
                ability
            )
            for ability in ABILITY_NAMES
        },
        skill_modifiers={
            skill: character.skill_modifier(skill)
            for skill in SKILL_ABILITIES
        },
        proficiency_bonus=character.proficiency_bonus,
        initiative=character.initiative,
        passive_perception=character.passive_perception,
        spell_attack_modifier=spell_attack_modifier,
        spell_save_dc=spell_save_dc,
    )


def get_service(
    session: Session,
) -> CharacterService:
    return CharacterService(
        CharacterRepository(session)
    )


@router.post(
    "",
    response_model=CharacterResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_character(
    payload: CharacterCreateRequest,
    user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> CharacterResponse:
    try:
        character = from_request(payload)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(error),
        ) from error

    created = get_service(session).create(
        owner_id=user.id,
        character=character,
    )

    return to_response(created)


@router.get(
    "",
    response_model=list[CharacterResponse],
)
def list_characters(
    user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> list[CharacterResponse]:
    characters = get_service(session).list_for_owner(
        user.id
    )

    return [
        to_response(character)
        for character in characters
    ]


PORTRAIT_EXTENSIONS = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


@router.post(
    "/{character_id}/portrait",
    response_model=CharacterResponse,
)
async def upload_character_portrait(
    character_id: int,
    portrait: UploadFile = File(...),
    user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> CharacterResponse:
    try:
        extension = PORTRAIT_EXTENSIONS[
            portrait.content_type or ""
        ]
    except KeyError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=(
                "portrait must be JPEG, PNG, or WebP"
            ),
        ) from error

    service = get_service(session)

    try:
        character = service.get_for_owner(
            character_id=character_id,
            owner_id=user.id,
        )
    except CharacterNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="character not found",
        ) from error

    content = await portrait.read(
        settings.maximum_portrait_size + 1
    )

    if len(content) > settings.maximum_portrait_size:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="portrait must not exceed 5 MB",
        )

    character_directory = (
        settings.upload_directory
        / "characters"
        / str(character_id)
    )
    character_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = f"{uuid4().hex}{extension}"
    file_path = character_directory / filename
    file_path.write_bytes(content)

    character.portrait_url = (
        f"/uploads/characters/"
        f"{character_id}/{filename}"
    )

    updated = service.update_for_owner(
        character_id=character_id,
        owner_id=user.id,
        character=character,
    )

    return to_response(updated)

@router.get(
    "/{character_id}",
    response_model=CharacterResponse,
)
def get_character(
    character_id: int,
    user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> CharacterResponse:
    try:
        character = get_service(session).get_for_owner(
            character_id=character_id,
            owner_id=user.id,
        )
    except CharacterNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="character not found",
        ) from error

    return to_response(character)


@router.put(
    "/{character_id}",
    response_model=CharacterResponse,
)
def update_character(
    character_id: int,
    payload: CharacterCreateRequest,
    user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> CharacterResponse:
    try:
        character = from_request(payload)
        updated = get_service(session).update_for_owner(
            character_id=character_id,
            owner_id=user.id,
            character=character,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(error),
        ) from error
    except CharacterNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="character not found",
        ) from error

    return to_response(updated)


@router.delete(
    "/{character_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_character(
    character_id: int,
    user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> Response:
    try:
        get_service(session).delete_for_owner(
            character_id=character_id,
            owner_id=user.id,
        )
    except CharacterNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="character not found",
        ) from error

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )



@router.post(
    "/{character_id}/health/{action}",
    response_model=CharacterResponse,
)
def change_character_hit_points(
    character_id: int,
    action: str,
    payload: HitPointActionRequest,
    user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> CharacterResponse:
    try:
        character = get_service(
            session
        ).change_hit_points(
            character_id=character_id,
            owner_id=user.id,
            action=action,
            amount=payload.amount,
        )
    except CharacterNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="character not found",
        ) from error
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(error),
        ) from error

    return to_response(character)