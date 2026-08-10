from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.database.models.user import UserModel

from app.database.connection import get_db_session
from app.repositories.user import UserRepository
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.security.tokens import create_access_token
from app.services.authentication import (
    AuthenticationService,
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: RegisterRequest,
    session: Session = Depends(get_db_session),
) -> UserResponse:
    service = AuthenticationService(
        UserRepository(session)
    )

    try:
        user = service.register(
            email=str(payload.email),
            password=payload.password,
        )
    except EmailAlreadyRegisteredError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="email already registered",
        ) from error

    return UserResponse(
        id=user.id,
        email=user.email,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    payload: LoginRequest,
    session: Session = Depends(get_db_session),
) -> TokenResponse:
    service = AuthenticationService(
        UserRepository(session)
    )

    try:
        user = service.authenticate(
            email=str(payload.email),
            password=payload.password,
        )
    except InvalidCredentialsError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

    return TokenResponse(
        access_token=create_access_token(user.id),
    )

@router.get(
    "/me",
    response_model=UserResponse,
)
def current_user(
    user: UserModel = Depends(get_current_user),
) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
    )
