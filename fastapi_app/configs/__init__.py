"""Инициализация переменных проекта."""

from fastapi_app.configs.loguru_conf import logger
from fastapi_app.configs.main_conf import settings
from fastapi_app.configs.taskiq_broker import broker
from fastapi_app.configs.validate_env import validate_settings

__all__ = [
    "logger",
    "settings",
    "broker",
    "validate_settings",
]
