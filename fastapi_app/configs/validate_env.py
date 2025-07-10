"""Модуль для загрузки и проверки конфигурации приложения."""

from fastapi_app.configs.loguru_conf import logger
from fastapi_app.configs.main_conf import settings


def validate_settings() -> None:
    """
    Проверяет наличие и корректность основных параметров.

    Логгирует успешную загрузку или ошибку при валидации.
    """
    try:
        logger.info("Валидация конфигурации...")
        _ = settings.db.url
        _ = settings.taskiq.url
        _ = settings.auth_jwt.private_key_path
        _ = settings.auth_jwt.public_key_path
        logger.success("✅ Конфигурация успешно загружена из .env")
    except Exception as e:
        logger.error(f"❌ Ошибка валидации настроек: {e}")
        raise
