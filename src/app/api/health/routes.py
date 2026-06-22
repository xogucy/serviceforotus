from fastapi import APIRouter, status

from app.db.session import ping_database

router = APIRouter()


@router.get("/live", status_code=status.HTTP_200_OK)
@router.get("/health/live", status_code=status.HTTP_200_OK, include_in_schema=False)
async def live() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/", status_code=status.HTTP_200_OK, include_in_schema=False)
async def legacy_health() -> dict[str, str]:
    return {"status": "OK"}


@router.get("/ready", status_code=status.HTTP_200_OK)
@router.get("/health/ready", status_code=status.HTTP_200_OK, include_in_schema=False)
async def ready() -> dict[str, str]:
    await ping_database()
    return {"status": "ok"}
