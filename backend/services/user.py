from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from crud import UserCRUD
from db.models import User


class UserService:
    def __init__(self, crud: UserCRUD) -> None:
        self.crud = crud

    async def get_by_uuid(self, uuid: UUID, session: AsyncSession) -> User:
        user: User | None = await self.crud.get_by_uuid(uuid, session)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
