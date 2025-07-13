"""Создание пользователя."""

import pytest
from fastapi import status


@pytest.mark.asyncio
@pytest.mark.user
async def test_create_user(
    client,
):
    """Тест создания нового пользователя и проверка дубликатов."""
    payload = {
        "username": "uniqueuser",
        "email": "unique@mail.ru",
        "password": "password123",
        "password_confirm": "password123",
    }

    response = await client.post(
        "/api/v1/users/",
        json=payload,
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Повторный email
    response = await client.post(
        "/api/v1/users/",
        json={
            "username": "newuser",
            "email": payload["email"],
            "password": "password123",
            "password_confirm": "password123",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.json()["detail"].lower()

    # Повторный username
    response = await client.post(
        "/api/v1/users/",
        json={
            "username": payload["username"],
            "email": "new@mail.ru",
            "password": "password123",
            "password_confirm": "password123",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.json()["detail"].lower()

    # password_confirm не совпал с password
    response = await client.post(
        "/api/v1/users/",
        json={
            "username": "new_username",
            "email": "new@mail.ru",
            "password": "password123",
            "password_confirm": "password12345",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Passwords do not match"
