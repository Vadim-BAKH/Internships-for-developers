from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.crud.user_crud.create_user import create_user
from fastapi_app.schemas import UserCreate, UserRead
from fastapi_app.tasks import send_welcome_email


async def create_user_with_welcome_email(
    session: AsyncSession,
    data: UserCreate,
) -> UserRead:
    user = await create_user(session, data)
    await send_welcome_email.kiq(user_id=user.id)
    return UserRead.model_validate(user)
