"""Модуль авторизации пользователя."""

from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.authentication.jwt_utils import decode_jwt
from fastapi_app.authentication.token_utils import (
    ensure_refresh_token_type,
    ensure_access_token_type,
)

from fastapi_app.crud.user_crud.get_auth_user import get_user_by_username
from fastapi_app.database import get_session_db
from fastapi_app.exceptions import (
    InvalidToken,
    UserInActive,
)
from fastapi_app.models import User
from fastapi_app.configs import logger


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/jwt/login/",
)


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict[str, Any]:
    """Получает авторизованного пользователя по токену."""
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as ite:
        logger.warning("Получен недопустимый токен")
        raise InvalidToken() from ite
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_session_db),
) -> User:
    """Получает username из payload по ключу sub."""
    ensure_access_token_type(payload=payload)
    username: str | None = payload.get("sub")
    if not username:
        logger.warning("Access-токен не содержит поля 'sub'")
        raise InvalidToken()

    user = await get_user_by_username(
        username=username,
        session=session,
    )
    if not user:
        logger.warning("Пользователь с username '{}' не найден", username)
        raise InvalidToken()
    return user


async def get_current_refresh_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_session_db),
) -> User:
    """
    Получает пользователя по refresh-токену.

    Проверяет тип токена.
    Извлекает username и возвращает пользователя из базы.
    Бросает исключения при невалидном токене или неправильном типе.
    """
    ensure_refresh_token_type(payload=payload)
    username = payload.get("sub")
    if not username:
        logger.warning("Refresh-токен не содержит поля 'sub'")
        raise InvalidToken()
    user = await get_user_by_username(
        username=username,
        session=session,
    )
    if not user:
        logger.warning("Пользователь с username '{}' не найден", username)
        raise InvalidToken()
    return user


async def get_active_auth_user(
    user: User = Depends(get_current_auth_user),
) -> User:
    """
    Получает только активного пользователя.

    Выбрасывает исключение, если пользователь архивирован.
    """
    if not user.is_active:
        logger.warning("Пользователь '{}' неактивен", user.username)
        raise UserInActive()
    return user
