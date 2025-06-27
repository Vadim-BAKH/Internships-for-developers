"""Главный конфигуратор сервисов."""

import logging
from typing import Literal

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

LOGURU_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


class DatabaseConfig(BaseModel):
    """Модель pydantic базы данных."""

    url: PostgresDsn
    echo: bool = False
    pool_size: int = 20
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class LoggingConfig(BaseModel):
    """Модель pydantic логирования."""

    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"
    format: str = LOGURU_FORMAT

    @property
    def level_value(self) -> int:
        """Возвращает цифровой идентификатор уровня."""
        return logging.getLevelNamesMapping()[self.level.upper()]


class AppConfig(BaseModel):
    """Конфигурация приложения."""

    api_prefix: str = "/api"


class Settings(BaseSettings):
    """Базовый конфигуратор приложения."""

    db: DatabaseConfig
    logging: LoggingConfig = LoggingConfig()
    app: AppConfig = AppConfig()

    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore",
    )


settings = Settings()
