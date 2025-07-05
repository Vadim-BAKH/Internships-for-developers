"""Инициализация маршрутов приложения."""

from fastapi_app.routers.jwt import router as auth_rout
from fastapi_app.routers.user import router as user_rout

__all__ = [
    "user_rout",
    "auth_rout",
]
