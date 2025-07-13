"""Получение пользователя по ID."""

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.exceptions import NoUserByThisId
from fastapi_app.models import User


async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
) -> User:
    """Получает из сессии пользователя по ID."""
    user = await session.get(User, user_id)
    if not user:
        raise NoUserByThisId()

    return user
