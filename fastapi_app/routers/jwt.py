"""Маршруты для авторизации пользователя через JWT-токен."""

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer

from fastapi_app.authentication import (
    create_access_token,
    create_refresh_token,
    validate_auth_user,
)
from fastapi_app.authentication.auth_user import (
    get_active_auth_user,
    get_current_refresh_user,
)
from fastapi_app.configs import settings
from fastapi_app.models import User
from fastapi_app.schemas import TokenInfo, UserAuthSchema

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/jwt",
    tags=["YWT"],
    dependencies=[Depends(http_bearer)],
)


@router.post(
    "/login/",
    response_model=TokenInfo,
    status_code=status.HTTP_200_OK,
)
async def auth_user_issue_jwt(
    user: User = Depends(validate_auth_user),
):
    """
    Авторизация пользователя и выдача JWT-токена.

    Проверяет логин и пароль, генерирует:
           - access_token;
           - refresh_token.
    """
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
        expires_in=settings.auth_jwt.access_token_expire_minutes * 60,
    )


@router.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
async def auth_refresh_jwt(
    user: User = Depends(get_current_refresh_user),
) -> TokenInfo:
    """Обновляет access-токен по refresh-токену."""
    access_token = create_access_token(user=user)
    return TokenInfo(
        access_token=access_token,
        token_type="Bearer",
        expires_in=settings.auth_jwt.access_token_expire_minutes * 60,
    )


@router.get(
    "/users/me/",
    response_model=UserAuthSchema,
    status_code=status.HTTP_200_OK,
)
async def get_auth_user_self_info(
    user: User = Depends(get_active_auth_user),
) -> UserAuthSchema:
    """
    Возвращает информацию о текущем авторизованном пользователе.

    Требуется валидный JWT-токен.
    """
    return UserAuthSchema.model_validate(user)
