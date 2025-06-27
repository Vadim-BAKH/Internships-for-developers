"""
Конфигурационные переменные проекта:
- settings: глобальные настройки из .env
- logger: сконфигурированный loguru
- TEST_DB_URL: строка подключения к тестовой БД
"""

from fastapi_app.configs.loguru_conf import logger
from fastapi_app.configs.main_conf import settings

__all__ = [
    "logger",
    "settings",
]
