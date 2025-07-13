"""Обновление access-токена через refresh-токен."""

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.auth
async def test_refresh_token_issues_new_access_token(
    client: AsyncClient,
    create_user,
):
    """Проверяет успешное обновление access-токена через refresh-токен."""
    user = await create_user(
        username="refreshuser",
        email="refresh@example.com",
        password="refreshpass123",
    )

    # Авторизация — получение access и refresh токенов
    response = await client.post(
        "/api/v1/jwt/login/",
        data={
            "username": user["username"],
            "password": user["password"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == status.HTTP_200_OK
    tokens = response.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    # Обновление токена
    response = await client.post(
        "/api/v1/jwt/refresh/",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    new_access_token = response.json()["access_token"]
    assert new_access_token != access_token

    # Проверка доступа с новым токеном
    response = await client.get(
        "/api/v1/jwt/users/me/",
        headers={"Authorization": f"Bearer {new_access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == user["username"]
