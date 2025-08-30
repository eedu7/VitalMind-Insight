from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from db.models.user import User
from services import UserService

from .services import services


async def get_current_active_user(
    request: Request,
    user_service: UserService = Depends(services.get_user_service),
    session: AsyncSession = Depends(get_session),
) -> User:
    return await user_service.get_by_uuid(request.user.uuid, session)
