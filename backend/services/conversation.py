from typing import Sequence
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from crud.conversation import ConversationCRUD
from db.models import Conversation
from services.llm import LLMManager


class ConversationService:
    def __init__(self, crud: ConversationCRUD, llm: LLMManager) -> None:
        self.crud = crud
        self.llm = llm

    async def get_all_conversations(self, user_id: int, session: AsyncSession) -> Sequence[Conversation]:
        return await self.crud.get_all_by_filters(
            filters={"user_id": user_id},
            session=session,
        )

    async def get_conversation_by_uuid(self, uuid: UUID, session: AsyncSession) -> Conversation:
        conversation: Conversation | None = await self.crud.get_by_uuid(uuid, session)

        if not conversation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No conversation found")

        return conversation

    async def create_conversation(self, title: str, user_id: int, session: AsyncSession) -> Conversation:
        try:
            llm_generated_title = await self.llm.generate_title(title)

            conversation: Conversation = Conversation(user_id=user_id, title=llm_generated_title)

            await self.crud.create(conversation, session)

            return conversation
        except SQLAlchemyError as e:
            raise ValueError("Database error: {e}") from e

    async def delete_conversation(self, uuid: UUID, session: AsyncSession) -> None:
        conversation = await self.crud.get_by_uuid(uuid, session)

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No conversation found with the uuid {uuid}",
            )

        await self.crud.delete(conversation, session=session)

    async def update_conversation(self, uuid: UUID, title: str, session: AsyncSession) -> None:
        values = {"title": title}
        updated = await self.crud.update_by_uuid(uuid, values, session)

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No conversation found with the uuid {uuid}",
            )
