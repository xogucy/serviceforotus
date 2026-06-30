import httpx


class BillingClientError(RuntimeError):
    pass


class BillingClient:
    def __init__(self, base_url: str, timeout: float = 5.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def create_account(self, user_id: int | str) -> None:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/accounts",
                    json={"userId": str(user_id)},
                )
                response.raise_for_status()
        except httpx.HTTPError as error:
            raise BillingClientError("Could not create billing account") from error
