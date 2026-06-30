"""Users service layer."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate, UserUpdate


class UserAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = UserRepository(session)

    async def create_registered_user(
        self, payload: UserCreate, password_hash: str
    ) -> User:
        try:
            return await self.repository.create_registered_user(
                payload, password_hash=password_hash
            )

        except IntegrityError as exc:
            await self.repository.session.rollback()
            raise UserAlreadyExistsError from exc

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError
        return user

    async def get_user_by_username(self, username: str) -> User:
        user = await self.repository.get_by_username(username)
        if user is None:
            raise UserNotFoundError
        return user

    async def list_users(self) -> list[User]:
        return await self.repository.list()

    async def update_user(self, user_id: int, payload: UserUpdate) -> User:
        user = await self.get_user_by_id(user_id)
        try:
            return await self.repository.update(user, payload)
        except IntegrityError as exc:
            await self.repository.session.rollback()
            raise UserAlreadyExistsError from exc

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user_by_id(user_id)
        await self.repository.delete(user)
