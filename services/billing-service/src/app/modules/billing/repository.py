from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.billing.models import Account


class AccountAlreadyExistsError(RuntimeError):
    pass


class BillingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_account(self, user_id: str) -> Account:
        account = Account(user_id=user_id, balance=Decimal("0"))
        self.session.add(account)

        try:
            await self.session.commit()
        except IntegrityError as error:
            await self.session.rollback()
            raise AccountAlreadyExistsError(user_id) from error

        await self.session.refresh(account)
        return account

    async def get_account_by_user_id(self, user_id: str) -> Account | None:
        result = await self.session.execute(
            select(Account).where(Account.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def add_money(self, user_id: str, amount: Decimal) -> Account | None:
        account = await self.get_account_by_user_id_for_update(user_id)
        if account is None:
            return None

        account.balance += amount
        await self.session.commit()
        await self.session.refresh(account)
        return account

    async def withdraw_money(
        self,
        user_id: str,
        amount: Decimal,
    ) -> tuple[Account | None, bool]:
        account = await self.get_account_by_user_id_for_update(user_id)
        if account is None:
            return None, False

        if account.balance < amount:
            return account, False

        account.balance -= amount
        await self.session.commit()
        await self.session.refresh(account)
        return account, True

    async def get_account_by_user_id_for_update(self, user_id: str) -> Account | None:
        result = await self.session.execute(
            select(Account).where(Account.user_id == user_id).with_for_update()
        )
        return result.scalar_one_or_none()
