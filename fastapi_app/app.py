"""Приложение FastApi."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from fastapi_app.configs import settings
from fastapi_app.database import async_engine
from fastapi_app.routers import user_rout


@asynccontextmanager
async def database_life_cycle(app: FastAPI) -> AsyncIterator:
    """
    Асинхронное соединение с базой движка.

    Устанавливает и закрывает соединение.
    """

    yield
    await async_engine.dispose()


app_ = FastAPI(
    lifespan=database_life_cycle,
    default_response_class=ORJSONResponse,
)

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

app_.include_router(
    user_rout,
    prefix=f"{settings.app.api_prefix}",
)
