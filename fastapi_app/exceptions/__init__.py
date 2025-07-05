"""Инициализация исключений."""

from fastapi_app.exceptions.bad_request import (
    EmailExists,
    PasswordsDoNotMatch,
    UsernameExists,
)
from fastapi_app.exceptions.forbidden import UserInActive
from fastapi_app.exceptions.general_errors import register_exception_handler
from fastapi_app.exceptions.unauthorizes import InvalidToken, UserUnauthorized

__all__ = [
    "UsernameExists",
    "EmailExists",
    "UserUnauthorized",
    "register_exception_handler",
    "PasswordsDoNotMatch",
    "UserInActive",
    "InvalidToken",
]
