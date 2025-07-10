"""Инициализация задач taskiq."""

import sys

from fastapi_app.configs import logger
from fastapi_app.tasks.welcom_email_notification import send_welcome_email

__all__ = [
    "send_welcome_email",
]
if "taskiq" in sys.argv[0]:
    logger.info("Taskiq worker загружает задачи")
else:
    logger.debug(f"Задачи загружены в процессе: {sys.argv[0]}")
