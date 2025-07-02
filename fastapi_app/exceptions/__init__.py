"""Инициализация исключений."""

from fastapi_app.exceptions.bad_request import EmailExists, UsernameExists
from fastapi_app.exceptions.general_errors import register_exception_handler

__all__ = [
    "UsernameExists",
    "EmailExists",
    "register_exception_handler",
]
