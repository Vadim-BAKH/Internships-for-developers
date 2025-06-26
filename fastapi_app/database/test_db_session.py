"""Настройки тестового и движка и сессий."""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from fastapi_app.configs import TEST_DB_URL

test_async_engine = create_async_engine(TEST_DB_URL)
test_async_session = async_sessionmaker(
    bind=test_async_engine,
    expire_on_commit=False,
)
