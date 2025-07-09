"""Маршруты пользователя."""

from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.crud import create_user
from fastapi_app.database import get_session_db
from fastapi_app.schemas import UserCreate, UserRead

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
    background_tasks: BackgroundTasks,
):
    """
    Создаёт пользователя.

    Проверяет уникальность username и email.
    Передаёт зависимость BackgroundTasks для отправки email.
    """
    return await create_user(
        session=session,
        data=user_in,
        background_tasks=background_tasks,
    )
