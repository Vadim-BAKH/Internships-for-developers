"""Схема токена."""

from pydantic import BaseModel


class TokenInfo(BaseModel):

    """Моделирует токен."""

    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int
