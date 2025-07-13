"""Модель пользователя."""

from sqlalchemy import LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from fastapi_app.models.base import BaseModel
from fastapi_app.models.mixins.pk_mix import IntIdPkMixin
from fastapi_app.models.mixins.soft_delete import ActiveMixin


class User(IntIdPkMixin, ActiveMixin, BaseModel):

    """Таблица пользователя."""

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    password: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False,
    )
