"""Инициализация исключений."""

from fastapi_app.exceptions.bad_request import (
    EmailExists,
    PasswordsDoNotMatch,
    UsernameExists,
)
from fastapi_app.exceptions.forbidden import UserInActive
from fastapi_app.exceptions.general_errors import register_exception_handler
from fastapi_app.exceptions.not_found import NoUserByThisId
from fastapi_app.exceptions.unauthorized import (
    InvalidToken,
    NotAccessTokenType,
    NotRefreshTokenType,
    UserUnauthorized,
)

__all__ = [
    "UsernameExists",
    "EmailExists",
    "UserUnauthorized",
    "register_exception_handler",
    "PasswordsDoNotMatch",
    "UserInActive",
    "InvalidToken",
    "NotAccessTokenType",
    "NotRefreshTokenType",
    "NoUserByThisId",
]
