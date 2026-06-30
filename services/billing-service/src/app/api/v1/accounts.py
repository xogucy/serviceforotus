from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.modules.billing.repository import BillingRepository
from app.modules.billing.schemas import (
    AccountResponse,
    CreateAccountRequest,
    MoneyOperationRequest,
    PaymentResultResponse,
)
from app.modules.billing.service import (
    AccountConflictError,
    AccountNotFoundError,
    BillingService,
)

router = APIRouter()


def get_billing_service(
    session: AsyncSession = Depends(get_session),
) -> BillingService:
    repository = BillingRepository(session)
    return BillingService(repository)


@router.post(
    "",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_account(
    payload: CreateAccountRequest,
    service: BillingService = Depends(get_billing_service),
) -> AccountResponse:
    try:
        return await service.create_account(payload)
    except AccountConflictError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.get("/{user_id}", response_model=AccountResponse)
async def get_account(
    user_id: str,
    service: BillingService = Depends(get_billing_service),
) -> AccountResponse:
    try:
        return await service.get_account(user_id)
    except AccountNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.post("/{user_id}/deposit", response_model=AccountResponse)
async def deposit(
    user_id: str,
    payload: MoneyOperationRequest,
    service: BillingService = Depends(get_billing_service),
) -> AccountResponse:
    try:
        return await service.deposit(user_id, payload)
    except AccountNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.post("/{user_id}/withdraw", response_model=PaymentResultResponse)
async def withdraw(
    user_id: str,
    payload: MoneyOperationRequest,
    service: BillingService = Depends(get_billing_service),
) -> PaymentResultResponse:
    try:
        return await service.withdraw(user_id, payload)
    except AccountNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
