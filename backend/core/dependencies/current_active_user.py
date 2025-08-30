from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from crud import UserCRUD
from db import get_session
from db.models.user import User
from services import UserService

crud = UserCRUD()
user_service = UserService(crud)


async def get_current_active_user(request: Request, session: AsyncSession = Depends(get_session)) -> User:
    return await user_service.get_by_uuid(request.user.id, session)
