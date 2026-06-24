from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.modules.auth.schemas import LoginRequest, RegisterRequest, TokenResponse
from app.modules.auth.service import AuthService, InvalidCredentialsError
from app.modules.users.service import UserAlreadyExistsError

router = APIRouter(tags=["auth"])


def get_auth_service(
    session: AsyncSession = Depends(get_db_session),
) -> AuthService:
    return AuthService(session)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
):
    try:
        user = await service.register_user(payload)
    except UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username or email already exists",
        ) from exc
    return {
        "id": user.id,
        "username": user.username,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "email": user.email,
        "phone": user.phone,
    }


@router.post("/login", response_model=TokenResponse)
async def login_user(
    payload: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    try:
        access_token = await service.login_user(payload)
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        ) from exc
    return TokenResponse(access_token=access_token)
