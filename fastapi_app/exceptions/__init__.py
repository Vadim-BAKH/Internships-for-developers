"""Инициализация исключений."""

from fastapi_app.exceptions.bad_request import EmailExists, UsernameExists

__all__ = [
    "UsernameExists",
    "EmailExists",
]
