"""Задача Taskiq для отправки приветственного письма пользователю."""

from taskiq import TaskiqDepends

from fastapi_app.configs import broker, logger
from fastapi_app.database import get_session_db
from fastapi_app.mailing.welcome_email import (
    welcome_email as send,
)


@broker.task
async def send_welcome_email(
    user_id: int,
    session=TaskiqDepends(get_session_db),
) -> None:
    """
    Асинхронная задача Taskiq для отправки приветственного письма.

    Логгирует процесс отправки и вызывает функцию отправки письма.
    Аргументы:
        user_id (int): Идентификатор пользователя, которому отправляется письмо;
        session: Асинхронная сессия базы данных, через зависимость TaskiqDepends.
    """
    logger.info("Sending welcome email to user '{}'", user_id)
    await send(user_id=user_id, session=session)
