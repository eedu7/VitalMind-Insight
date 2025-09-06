from typing import Sequence
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

    async def get_message_by_uuid(self, message_uuid: UUID, session: AsyncSession) -> Message:
        try:
            message = await self.crud.get_by_uuid(message_uuid, session)
            if message:
                return message
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}")

    async def get_messages_by_conversation_uuid(
        self, conversation_uuid: UUID, session: AsyncSession
    ) -> Sequence[Message]:
        try:
            return await self.crud.get_by_conversation_uuid(conversation_uuid, session=session)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}")

    async def update_message(self, message_uuid: UUID, role: Role, content: str, session: AsyncSession):
        try:
            updated = await self.crud.update_by_uuid(
                uuid=message_uuid, values={"role": role, "content": content}, session=session
            )

            if not updated:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in updating")

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}")

    async def delete_message(self, message_uuid: UUID, session: AsyncSession):
        try:
            message: Message = await self.get_message_by_uuid(message_uuid, session)

            await self.crud.delete(message, session)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}")
