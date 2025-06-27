"""Создание пользователя."""

import pytest
from pydantic import EmailStr

from fastapi_app.crud import create_user
from fastapi_app.exceptions import EmailExists, UsernameExists
from fastapi_app.schemas import UserCreate


@pytest.mark.asyncio
@pytest.mark.user
async def test_create_user(
    db_session,
):
    """Тестируем создание пользователя."""
    username: str = "Тестовое имя"
    email: EmailStr = "test@mail.ru"

    user_data = UserCreate(
        username=username,
        email=email,
    )

    # Создаём пользователя
    created_user = await create_user(
        session=db_session,
        data=user_data,
    )

    assert created_user.username == username
    assert created_user.email == email
    assert created_user.id is not None

    with pytest.raises(UsernameExists):
        await create_user(session=db_session, data=user_data)

    with pytest.raises(EmailExists):
        await create_user(
            session=db_session,
            data=UserCreate(username="другое_имя", email=email),
        )
