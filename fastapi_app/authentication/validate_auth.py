"""Валидация пользователя при авторизации."""

from fastapi import Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.authentication.jwt_utils import validate_password
from fastapi_app.crud.user_crud.get_auth_user import get_user_by_username
from fastapi_app.database import get_session_db
from fastapi_app.exceptions import UserUnauthorized
from fastapi_app.models import User


async def validate_auth_user(
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_session_db),
) -> User:
    """
    Валидация пользователя для авторизации.

    Получает через форму username/password.
    Проверяет наличие в базе username.
    Проверяет совпадение пароля.
    Возвращает пользователя из модели.
    """
    user: User = await get_user_by_username(
        session=session,
        username=username,
    )
    if not user:
        raise UserUnauthorized()

    if not validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise UserUnauthorized()

    return user
