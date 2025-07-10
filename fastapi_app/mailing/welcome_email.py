"""Приветствие новому пользователю."""

from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends

from fastapi_app.crud.user_crud.get_by_id import get_user_by_id
from fastapi_app.mailing.send_email import send_email


async def welcome_email(
    user_id: int,
    session: Annotated[
        AsyncSession,
        TaskiqDepends,
    ],
):
    """Фоновая задача — отправка письма."""
    user = await get_user_by_id(
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
