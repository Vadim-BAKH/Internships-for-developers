"""Получение пользователя по username."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.models import User


async def get_user_by_username(
    username: str,
    session: AsyncSession,
) -> User | None:
    """Возвращает пользователя по username или None, если не найден."""
    user_query = await session.execute(
        select(User).where(User.username == username)
    )
    return user_query.scalar_one_or_none()
