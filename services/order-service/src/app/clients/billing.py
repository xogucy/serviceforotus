from decimal import Decimal

import httpx
from pydantic import BaseModel


class BillingClientError(RuntimeError):
    pass


class BillingPaymentResult(BaseModel):
    success: bool
    userId: str
    balance: Decimal
    reason: str | None = None


class BillingClient:
    def __init__(self, base_url: str, timeout: float = 5.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def withdraw(self, user_id: str, amount: Decimal) -> BillingPaymentResult:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/accounts/{user_id}/withdraw",
                    json={"amount": str(amount)},
                )
                response.raise_for_status()
        except httpx.HTTPError as error:
            raise BillingClientError("Could not withdraw money") from error

        return BillingPaymentResult.model_validate(response.json())
