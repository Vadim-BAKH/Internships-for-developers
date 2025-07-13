"""Утилиты для проверки токена."""

from fastapi_app.authentication.create_token import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
)
from fastapi_app.configs import logger
from fastapi_app.exceptions import NotAccessTokenType, NotRefreshTokenType


def ensure_access_token_type(payload: dict) -> None:
    """Убедиться, что тип токена — access."""
    if payload.get(TOKEN_TYPE_FIELD) != ACCESS_TOKEN_TYPE:
        logger.warning("Ожидался access token, но тип другой.")
        raise NotAccessTokenType()


def ensure_refresh_token_type(payload: dict) -> None:
    """Убедиться, что тип токена — refresh."""
    if payload.get(TOKEN_TYPE_FIELD) != REFRESH_TOKEN_TYPE:
        logger.warning("Ожидался refresh token, но тип другой.")
        raise NotRefreshTokenType()
