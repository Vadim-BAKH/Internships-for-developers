"""Конфигурация loguru."""

import sys

from loguru import logger

from fastapi_app.configs.main_conf import settings

logger.remove()
logger.add(
    sink=sys.stdout,
    format=settings.logging.format,
    level=settings.logging.level,
    enqueue=True,
    backtrace=True,  # полезно в dev
    diagnose=True,  # показывает локальные переменные при ошибках
)
