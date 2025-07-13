"""Базовая модель."""

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from fastapi_app.configs import settings
from fastapi_app.utils import camel_case_to_snake_case


class Base(DeclarativeBase):

    """Базовый класс для декларативных моделей SQLAlchemy."""

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )


class BaseModel(Base):

    """Абстрактная модель с общими свойствами для всех таблиц."""

    __abstract__ = True

    @declared_attr  # pylint: disable=no-self-argument
    def __tablename__(cls) -> str:
        """Формирует название таблицы с s на-конце."""
        return f"{camel_case_to_snake_case(cls.__name__)}s"

    def __repr__(self) -> str:
        """Строковое представление id и имени моделей."""
        id_val = getattr(self, "id", None)
        name_val = getattr(self, "name", None)
        return f"<{self.__class__.__name__} pk={id_val} | name: {name_val}>"
