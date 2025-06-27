"""Инициализация запросов CRUD."""

from fastapi_app.crud.user_crud.check_email import check_email
from fastapi_app.crud.user_crud.check_username import check_name
from fastapi_app.crud.user_crud.create_user import create_user

__all__ = [
    "create_user",
    "check_name",
    "check_email",
]
