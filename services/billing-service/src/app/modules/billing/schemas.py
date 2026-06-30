from decimal import Decimal

from pydantic import BaseModel, Field


class CreateAccountRequest(BaseModel):
    userId: str = Field(min_length=1)


class MoneyOperationRequest(BaseModel):
    amount: Decimal = Field(gt=0)


class AccountResponse(BaseModel):
    userId: str
    balance: Decimal


class PaymentResultResponse(BaseModel):
    success: bool
    userId: str
    balance: Decimal
    reason: str | None = None
