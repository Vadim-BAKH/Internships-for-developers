"""Создание пользователя."""

import pytest
from fastapi import status


@pytest.mark.asyncio
@pytest.mark.user
async def test_create_user(
    client,
):
    """Тестируем создание пользователя."""
    user_payload = {
        "username": "uniqueuser",
        "email": "unique@mail.ru",
    }

    # Первый запрос — успешное создание
    response = await client.post(
        "/api/users/",
        json=user_payload,
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Второй запрос с тем же email — должен вернуть ошибку
    response_email = await client.post(
        "/api/users/",
        json={
            "username": "anotheruser",
            "email": user_payload["email"],
        },
    )
    assert response_email.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response_email.json().get("detail", "").lower()

    # Третий запрос с тем же username — тоже ошибка
    response_username = await client.post(
        "/api/users/",
        json={
            "username": user_payload["username"],
            "email": "another@mail.ru",
        },
    )
    assert response_username.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response_username.json().get("detail", "").lower()
