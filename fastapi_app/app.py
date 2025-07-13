"""Приложение FastApi."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from fastapi_app.configs import (
    broker,
    settings,
    validate_settings,
)
from fastapi_app.database import async_engine
from fastapi_app.exceptions import register_exception_handler
from fastapi_app.routers import auth_rout, user_rout

validate_settings()


@asynccontextmanager
async def database_life_cycle(app: FastAPI) -> AsyncIterator:
    """
    Асинхронное соединение с базой движка.

    Устанавливает и закрывает соединение.
    """
    if not broker.is_worker_process:
        await broker.startup()
    yield
    await async_engine.dispose()
    if not broker.is_worker_process:
        await broker.shutdown()


app_ = FastAPI(
    lifespan=database_life_cycle,
    default_response_class=ORJSONResponse,
)

register_exception_handler(app_)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
app_.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # разрешённые источники
    allow_credentials=True,
    allow_methods=["*"],  # разрешённые HTTP методы
    # allow_headers=["*"],
    allow_headers=["Content-Type", "X-My-Fancy-Header"],
    expose_headers=["Content-Type", "X-Custom-Header"],
)

API_PREFIX_V1 = f"{settings.app.api_prefix}{settings.app.v1.prefix}"

app_.include_router(user_rout, prefix=API_PREFIX_V1)
app_.include_router(auth_rout, prefix=API_PREFIX_V1)
