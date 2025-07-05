"""Маршруты для авторизации пользователя через JWT-токен."""

from fastapi import APIRouter, Depends, status

from fastapi_app.authentication import encode_jwt, validate_auth_user
from fastapi_app.authentication.auth_user import get_active_auth_user
from fastapi_app.models import User
from fastapi_app.schemas import TokenInfo, UserAuthSchema

router = APIRouter(prefix="/jwt", tags=["YWT"])


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

    Проверяет логин и пароль, генерирует access token.
    """
    jwt_payload = {
        "sub": user.username,
        "email": user.email,
    }
    token = encode_jwt(jwt_payload)

    return TokenInfo(
        access_token=token,
        token_type="Bearer",
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
