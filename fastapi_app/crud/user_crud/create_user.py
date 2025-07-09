"""Создаёт нового пользователя."""

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.authentication import hash_password
from fastapi_app.configs import logger
from fastapi_app.crud.user_crud.check_email import check_email
from fastapi_app.crud.user_crud.check_username import check_name
from fastapi_app.mailing import send_welcome_email
from fastapi_app.models import User
from fastapi_app.schemas import UserCreate, UserRead


async def create_user(
    session: AsyncSession,
    data: UserCreate,
    background_tasks: BackgroundTasks,
) -> UserRead:
    """
    Создаёт пользователя с уникальным username и email.

    Отправляет фоновый send_welcome_email.
    """
    logger.debug(
        "Creating username: '{}'",
        data.username,
    )
    logger.debug(
        "Creating email: '{}'",
        data.email,
    )

    await check_name(
        session=session,
        username=data.username,
    )
    await check_email(
        session=session,
        email=data.email,
    )
    hashed_password = hash_password(
        data.password.get_secret_value(),
    )
    new_user = User(
        username=data.username,
        email=data.email,
        password=hashed_password,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    background_tasks.add_task(send_welcome_email, user_id=new_user.id)

    logger.info(
        "User created successfully: '{}'",
        new_user.username,
    )
    return UserRead.model_validate(new_user)
