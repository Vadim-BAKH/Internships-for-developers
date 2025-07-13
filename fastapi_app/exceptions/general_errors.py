"""Регистрация исключений."""

from aiosmtplib.errors import SMTPConnectError
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import DatabaseError, IntegrityError, OperationalError

from fastapi_app.configs import logger


def register_exception_handler(app: FastAPI) -> None:
    """Регистрирует общие исключения."""

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(
        request: Request,
        exc: RequestValidationError,
    ) -> ORJSONResponse:
        """Обработка ошибок валидации запросов FastAPI."""
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Request data is not correct",
                "errors": exc.errors(),
            },
        )

    @app.exception_handler(ValidationError)
    async def handle_pydantic_validation_error(
        request: Request,
        exc: ValidationError,
    ) -> ORJSONResponse:
        """Обработка ошибок валидации Pydantic моделей."""
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Data validation error",
                "errors": exc.errors(),
            },
        )

    @app.exception_handler(IntegrityError)
    async def handle_integrity_error(
        request: Request,
        exc: IntegrityError,
    ) -> ORJSONResponse:
        """Обработка ошибок ограничений базы данных."""
        logger.error("Database integrity error", exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "Database integrity error",
                "error": str(exc.orig) if exc.orig else str(exc),
            },
        )

    @app.exception_handler(OperationalError)
    async def handle_operational_error(
        request: Request,
        exc: OperationalError,
    ) -> ORJSONResponse:
        """Обработка ошибки подключения, таймаута."""
        logger.error("Database operational error", exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Database operational error",
            },
        )

    @app.exception_handler(DatabaseError)
    async def handle_database_error(
        request: Request,
        exc: DatabaseError,
    ) -> ORJSONResponse:
        """Обрабатывает общий класс ошибок базы."""
        logger.error("Unhandled database error", exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "An unexpected database error has occurred",
            },
        )

    @app.exception_handler(SMTPConnectError)
    async def handle_smtp_connect_error(
        request: Request,
        exc: SMTPConnectError,
    ) -> ORJSONResponse:
        """Обработка ошибки подключения к SMTP серверу."""
        logger.error("SMTP connection failed", exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "detail": "Unable to connect to mail server. Try again later.",
            },
        )

    @app.exception_handler(Exception)
    async def handle_generic_exception(
        request: Request,
        exc: Exception,
    ) -> ORJSONResponse:
        """Перехватывает все необработанные исключения."""
        logger.error("Unhandled exception", exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )
