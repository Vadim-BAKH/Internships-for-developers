"""Инициализация моделей."""

from fastapi_app.models.base import Base, BaseModel
from fastapi_app.models.mixins.pk_mix import IntIdPkMixin
from fastapi_app.models.mixins.soft_delete import ActiveMixin
from fastapi_app.models.user import User

__all__ = [
    "Base",
    "BaseModel",
    "IntIdPkMixin",
    "ActiveMixin",
    "User",
]
