"""Сериализатор пользователя."""

from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    SecretStr,
    model_validator,
)

from fastapi_app.exceptions import PasswordsDoNotMatch


class UserBase(BaseModel):

    """Базовая модель пользователя."""

    username: Annotated[str, MinLen(3), MaxLen(50)]
    email: EmailStr


class UserCreate(UserBase):

    """Создание пользователя с паролем."""

    password: Annotated[SecretStr, MinLen(8)]
    password_confirm: SecretStr

    @model_validator(mode="after")
    def passwords_match(cls, model):
        """Проверяет валидность второго пароля с первым."""
        if (
            model.password.get_secret_value()
            != model.password_confirm.get_secret_value()
        ):
            raise PasswordsDoNotMatch()
        return model


class UserRead(UserBase):

    """Ответ при получении пользователя."""

    model_config = ConfigDict(from_attributes=True)
    id: int


class UserAuthSchema(BaseModel):

    """Модель для авторизации (логина)."""

    model_config = ConfigDict(from_attributes=True)
    username: str
    email: EmailStr
    is_active: bool


class UserUpdateStatus(BaseModel):

    """Модель для обновления статуса пользователя."""

    username: str
    is_active: bool
