from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.modules.users.schemas import UserCreate, UserRead, UserUpdate
from app.modules.users.service import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UserService,
)

router = APIRouter(tags=["users"])


def serialize_user(user) -> UserRead:
    return UserRead(
        id=user.id,
        username=user.username,
        firstName=user.first_name,
        lastName=user.last_name,
        email=user.email,
        phone=user.phone,
        createdAt=user.created_at,
        updatedAt=user.updated_at,
    )


def get_user_service(
    session: AsyncSession = Depends(get_db_session),
) -> UserService:
    return UserService(session)


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
@router.post(
    "/user",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
async def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
):
    try:
        return serialize_user(await service.create_user(payload))
    except UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username or email already exists",
        ) from exc


@router.get("/users", response_model=list[UserRead])
async def list_users(service: UserService = Depends(get_user_service)):
    return [serialize_user(user) for user in await service.list_users()]


@router.get("/users/{user_id}", response_model=UserRead)
@router.get("/user/{user_id}", response_model=UserRead, include_in_schema=False)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    try:
        return serialize_user(await service.get_user(user_id))
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from exc


@router.put("/users/{user_id}", response_model=UserRead)
@router.put("/user/{user_id}", response_model=UserRead, include_in_schema=False)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    try:
        return serialize_user(await service.update_user(user_id, payload))
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from exc
    except UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username or email already exists",
        ) from exc


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@router.delete(
    "/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False
)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    try:
        await service.delete_user(user_id)
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
