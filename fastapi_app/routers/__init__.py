"""Инициализация маршрутов приложения."""

from fastapi_app.routers.user import router as user_rout

__all__ = [
    "user_rout",
]
