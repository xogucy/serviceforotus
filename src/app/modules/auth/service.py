"""Auth service layer."""
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
import jwt
import bcrypt

from app.core.config import get_settings
from app.modules.auth.schemas import LoginRequest, RegisterRequest
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate
from app.modules.users.service import UserNotFoundError, UserService

settings = get_settings()


class InvalidCredentialsError(Exception):
    pass


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {
        "sub": str(user_id),
        "exp": expire,
    }
    return jwt.encode(
        payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
    )


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.user_service = UserService(session=session)

    async def register_user(self, payload: RegisterRequest) -> User:
        password = payload.password.encode("utf-8")
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
        user_payload = UserCreate(
            username=payload.username,
            firstName=payload.firstName,
            lastName=payload.lastName,
            email=payload.email,
            phone=payload.phone,
        )
        return await self.user_service.create_registered_user(
            user_payload,
            password_hash=hashed_password,
        )

    async def login_user(self, payload: LoginRequest) -> str:
        try:
            user = await self.user_service.get_user_by_username(
                username=payload.username
            )
        except UserNotFoundError as exc:
            raise InvalidCredentialsError from exc

        is_valid_password = bcrypt.checkpw(
            payload.password.encode("utf-8"),
            user.password_hash.encode("utf-8"),
        )
        if not is_valid_password:
            raise InvalidCredentialsError
        return create_access_token(user_id=user.id)
