"""Модели обработки исключений 'HTTP_400_BAD_REQUEST'."""

from fastapi import HTTPException, status
from pydantic import EmailStr


class UsernameExists(HTTPException):
    """Модель исключения 'UsernameAlreadyExists'."""

    def __init__(self, username: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{username}' already exists",
        )


class EmailExists(HTTPException):
    """Модель исключения 'EmailAlreadyExists'."""

    def __init__(self, email: EmailStr):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{email}' already exists",
        )
