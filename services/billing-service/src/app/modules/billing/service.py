from decimal import Decimal

from app.modules.billing.models import Account
from app.modules.billing.repository import (
    AccountAlreadyExistsError,
    BillingRepository,
)
from app.modules.billing.schemas import (
    AccountResponse,
    CreateAccountRequest,
    MoneyOperationRequest,
    PaymentResultResponse,
)


class AccountNotFoundError(RuntimeError):
    pass


class AccountConflictError(RuntimeError):
    pass


INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"


class BillingService:
    def __init__(self, repository: BillingRepository) -> None:
        self.repository = repository

    async def create_account(self, payload: CreateAccountRequest) -> AccountResponse:
        try:
            account = await self.repository.create_account(payload.userId)
        except AccountAlreadyExistsError as error:
            raise AccountConflictError(
                f"Account for user {payload.userId} exists"
            ) from error

        return self.to_account_response(account)

    async def get_account(self, user_id: str) -> AccountResponse:
        account = await self.repository.get_account_by_user_id(user_id)
        if account is None:
            raise AccountNotFoundError(f"Account for user {user_id} not found")

        return self.to_account_response(account)

    async def deposit(
        self,
        user_id: str,
        payload: MoneyOperationRequest,
    ) -> AccountResponse:
        account = await self.repository.add_money(user_id, payload.amount)
        if account is None:
            raise AccountNotFoundError(f"Account for user {user_id} not found")

        return self.to_account_response(account)

    async def withdraw(
        self,
        user_id: str,
        payload: MoneyOperationRequest,
    ) -> PaymentResultResponse:
        account, withdrawn = await self.repository.withdraw_money(
            user_id,
            payload.amount,
        )
        if account is None:
            raise AccountNotFoundError(f"Account for user {user_id} not found")

        if not withdrawn:
            return PaymentResultResponse(
                success=False,
                userId=account.user_id,
                balance=account.balance,
                reason=INSUFFICIENT_FUNDS,
            )

        return PaymentResultResponse(
            success=True,
            userId=account.user_id,
            balance=account.balance,
            reason=None,
        )

    @staticmethod
    def to_account_response(account: Account) -> AccountResponse:
        balance = Decimal(account.balance)
        return AccountResponse(userId=account.user_id, balance=balance)
