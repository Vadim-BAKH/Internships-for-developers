"""Конфигуратор тестов."""

from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.app import app_
from fastapi_app.database import (
    async_test_engine,
    async_test_session,
    get_session_db,
)
from fastapi_app.models import Base


@pytest.fixture(autouse=True)
async def override_dependencies():
    """Переопределяет основную сессию на тестовую."""

    async def override_get_db() -> AsyncGenerator[
        AsyncSession,
        None,
    ]:
        """Создает сессию для тестов."""
        async with async_test_session() as session:
            yield session

    app_.dependency_overrides[get_session_db] = override_get_db
    yield
    app_.dependency_overrides.clear()


@pytest.fixture
async def db_session() -> AsyncGenerator[
    AsyncSession,
    None,
]:
    """Возвращает тестовую сессию базы данных."""
    async with async_test_session() as session:
        yield session


@pytest.fixture(autouse=True)
async def test_database() -> AsyncGenerator:
    """Фикстура для управления миграциями."""
    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield

    finally:
        async with async_test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await async_test_engine.dispose()


@pytest.fixture
async def client():
    """Возвращает асинхронный клиент."""
    async with AsyncClient(
        transport=ASGITransport(app=app_),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture
def create_user(client: AsyncClient):
    """Фикстура для создания тестового пользователя через API."""

    async def _create_user(
        username: str = "testuser",
        email: str = "testuser@example.com",
        password: str = "strongpassword123",
    ):
        payload = {
            "username": username,
            "email": email,
            "password": password,
            "password_confirm": password,
        }

        response = await client.post(
            "/api/v1/users/",
            json=payload,
        )

        assert (
            response.status_code == 201
        ), f"Failed to create user: {response.text}"
        return payload

    return _create_user


@pytest.fixture(autouse=True)
def mock_send_welcome_email():
    """Автоматически мокаем отправку фоновой задачи."""
    with patch(
        "fastapi_app.tasks.send_welcome_email.kiq",
        new_callable=AsyncMock,
    ):
        yield
