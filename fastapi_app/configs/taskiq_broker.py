"""
Модуль инициализации брокера Taskiq с поддержкой FastAPI.

Настраивает брокер очередей, интеграцию с FastAPI.
Обработка событий запуска воркера.
"""

__all__ = ("broker",)

import taskiq_fastapi
from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker

from fastapi_app.configs.loguru_conf import logger
from fastapi_app.configs.main_conf import settings

broker = AioPikaBroker(
    url=str(settings.taskiq.url),
)

taskiq_fastapi.init(
    broker,
    "fastapi_app.app:app_",
)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_worker_startup(state: TaskiqState) -> None:
    """
    Асинхронный обработчик события запуска воркера Taskiq.

    Логгирует успешный запуск и текущее состояние воркера.
    """
    logger.info(
        "Worker startup complete, got state: '{}'",
        state,
    )
