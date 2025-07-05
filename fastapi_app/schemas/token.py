"""Схема токена."""

from pydantic import BaseModel


class TokenInfo(BaseModel):
    """Моделирует токен."""

    access_token: str
    token_type: str = "Bearer"
