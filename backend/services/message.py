from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from crud import MessageCRUD
from db.models.message import Message, Role


class MessageService:
    def __init__(self, crud: MessageCRUD) -> None:
        self.crud = crud

    async def create_message(self, conversation_uuid: UUID, content: str, role: Role, session: AsyncSession) -> Message:
        try:
            return await self.crud.create_message(conversation_uuid, role, content, session)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error in creating message {e}")
