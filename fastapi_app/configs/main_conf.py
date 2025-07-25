"""Главный конфигуратор сервисов."""

import logging
from pathlib import Path
from typing import Literal

from pydantic import AmqpDsn, BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

CERTS_DIR = Path("/app/certs")


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


class DBTestConfig(BaseModel):

    """Модель тестового url."""

    uri: str = "postgresql+asyncpg://test:test@test_db:5433/test_db"


class TaskiqConfig(BaseModel):

    """Модель управления задачами taskiq."""

    url: AmqpDsn


class LoggingConfig(BaseModel):

    """Модель pydantic логирования."""

    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"
    format: str = LOGURU_FORMAT

    @property
    def level_value(self) -> int:
        """Возвращает цифровой идентификатор уровня."""
        return logging.getLevelNamesMapping()[self.level.upper()]


class AuthJWT(BaseModel):

    """Модель JWT ключа."""

    private_key_path: Path = CERTS_DIR / "jwt-private.pem"
    public_key_path: Path = CERTS_DIR / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class ApiV1Prefix(BaseModel):

    """Конфигурации версии v1."""

    prefix: str = "/v1"


class AppConfig(BaseModel):

    """Конфигурация приложения."""

    api_prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class Settings(BaseSettings):

    """Базовый конфигуратор приложения."""

    db: DatabaseConfig
    logging: LoggingConfig = LoggingConfig()
    app: AppConfig = AppConfig()
    url_test: DBTestConfig = DBTestConfig()
    auth_jwt: AuthJWT = AuthJWT()
    taskiq: TaskiqConfig

    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore",
    )


settings = Settings()
