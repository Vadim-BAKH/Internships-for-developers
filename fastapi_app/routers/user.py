"""Маршруты пользователя."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.database import get_session_db
from fastapi_app.schemas import UserCreate, UserRead
from fastapi_app.services import (
    create_user_with_email as create,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

SessionDep = Annotated[
    AsyncSession,
    Depends(get_session_db),
]


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_user(
    user_in: UserCreate,
    session: SessionDep,
):
    """
    Создаёт пользователя.

    Проверяет уникальность username и email.
    Отправляет email с broker Taskiq.
    """
    return await create.create_user_with_welcome_email(
        session=session,
        data=user_in,
    )
