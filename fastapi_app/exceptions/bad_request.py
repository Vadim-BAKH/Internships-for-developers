"""Модели обработки исключений 'HTTP_400_BAD_REQUEST'."""

from fastapi import HTTPException, status
from pydantic import EmailStr


class UsernameExists(HTTPException):

    """Модель исключения 'UsernameAlreadyExists'."""

    def __init__(self, username: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )


class EmailExists(HTTPException):

    """Модель исключения 'EmailAlreadyExists'."""

    def __init__(self, email: EmailStr):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )


class PasswordsDoNotMatch(HTTPException):

    """Исключение при несовпадении паролей."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )
