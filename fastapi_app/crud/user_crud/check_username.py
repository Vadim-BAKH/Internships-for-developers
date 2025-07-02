"""Проверка уникальности username."""

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.configs import logger
from fastapi_app.exceptions import UsernameExists
from fastapi_app.models import User


async def check_name(
    session: AsyncSession,
    username: str,
) -> bool:
    """
    Проверяет уникальность username.

    Поднимает исключение, если уже существует имя.
    """
    existing_user = await session.scalar(
        select(exists().where(User.username == username))
    )
    if existing_user:
        logger.info("User with username '{}' already exists.", username)
        raise UsernameExists(username)
    logger.debug("Username '{}' is available", username)

    return True
