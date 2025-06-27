"""Сериализатор пользователя."""

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """Базовая модель пользователя."""

    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Модель создания пользователя."""


class UserRead(UserBase):
    """Модель сериализации пользователя."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
