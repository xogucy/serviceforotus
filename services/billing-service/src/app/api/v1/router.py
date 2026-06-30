from fastapi import APIRouter

from app.api.v1.accounts import router as accounts_router

router = APIRouter()
router.include_router(accounts_router, prefix="/accounts", tags=["accounts"])
