"""Тесты авторизации и получения информации о текущем пользователе."""

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.auth
async def test_login_and_get_me(
    client: AsyncClient,
    create_user,
):
    """Проверяет успешный вход и получение данных текущего пользователя."""
    user = await create_user(
        username="jwtuser",
        email="jwt@example.com",
        password="supersecret",
    )

    # Авторизация
    response = await client.post(
        "/api/v1/jwt/login/",
        data={
            "username": user["username"],
            "password": user["password"],
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]

    # Получение текущего пользователя
    response = await client.get(
        "/api/v1/jwt/users/me/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["username"] == user["username"]
    assert user_data["email"] == user["email"]
