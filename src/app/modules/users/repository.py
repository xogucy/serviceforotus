from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, payload: UserCreate) -> User:
        user = User(
            username=payload.username,
            first_name=payload.firstName,
            last_name=payload.lastName,
            email=payload.email,
            phone=payload.phone,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def list(self) -> list[User]:
        result = await self.session.execute(select(User).order_by(User.id))
        return list(result.scalars().all())

    async def update(self, user: User, payload: UserUpdate) -> User:
        values = payload.model_dump(exclude_unset=True)
        field_map = {
            "firstName": "first_name",
            "lastName": "last_name",
        }
        for field, value in values.items():
            setattr(user, field_map.get(field, field), value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()
