"""Приветствие новому пользователю."""

from typing import TYPE_CHECKING

from fastapi_app.crud.user_crud.get_by_id import get_user_by_id
from fastapi_app.database import async_session
from fastapi_app.mailing.send_email import send_email

if TYPE_CHECKING:
    from fastapi_app.models import User


async def send_welcome_email(user_id: int):
    """Фоновая задача — отправка письма."""
    async with async_session() as session:
        user: User = await get_user_by_id(
            session=session,
            user_id=user_id,
        )
        await send_email(
            recipient=user.email,
            subject="Welcome to Internship for developers! ⛵",
            body=(
                f"Hello, {user.username}!\n\n"
                "Welcome to the Internship for Developers platform.\n\n"
                "We’re excited to have you on board. Here, you’ll be able to:\n"
                "- Learn new technologies\n"
                "- Work on real projects\n"
                "- Grow your developer experience\n\n"
                "Good luck on your journey!\n"
                "— Your IFD Team"
            ),
        )
