"""Настройки тестового и движка и сессий."""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from fastapi_app.configs import logger, settings

logger.debug("Connecting to test database '{}':", settings.url_test.uri)
async_test_engine = create_async_engine(settings.url_test.uri)
async_test_session = async_sessionmaker(
    bind=async_test_engine,
    expire_on_commit=False,
)
