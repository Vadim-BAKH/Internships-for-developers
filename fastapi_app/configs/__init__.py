"""
Конфигурационные переменные проекта:
- settings: глобальные настройки из .env
- logger: сконфигурированный loguru
- TEST_DB_URL: строка подключения к тестовой БД
"""

from fastapi_app.configs.loguru_conf import logger
from fastapi_app.configs.main_conf import settings
from fastapi_app.configs.test_url import TEST_DB_URL

__all__ = [
    "logger",
    "settings",
    "TEST_DB_URL",
]
