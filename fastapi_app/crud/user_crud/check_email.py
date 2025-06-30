"""Проверка уникальности email."""

from fastapi_app.configs import logger
from fastapi_app.exceptions import EmailExists
from fastapi_app.models import User
from pydantic import EmailStr
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession


async def check_email(
    session: AsyncSession,
    email: EmailStr,
) -> bool:
    """
    Проверяет уникальность email.

    Поднимает исключение, если уже существует адрес.
    """
    existing_user = await session.scalar(
        select(exists().where(User.email == email))
    )
    if existing_user:
        logger.info("User with email '{}' already exists.", email)
        raise EmailExists(email)
    logger.debug("Email '{}' is available", email)

    return True
