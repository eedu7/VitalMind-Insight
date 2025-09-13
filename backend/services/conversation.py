from typing import Sequence
from uuid import UUID

import httpx
from fastapi import HTTPException, Request, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.security.auth_cookies_manager import AuthCookieKey
from crud.conversation import ConversationCRUD
from db.models import Conversation
from db.models.message import Role
from services.llm import LLMManager
from services.message import MessageService


class ConversationService:
    def __init__(self, crud: ConversationCRUD, llm: LLMManager, message_service: MessageService) -> None:
        self.crud = crud
        self.llm = llm
        self.message_service = message_service

    async def get_all_conversations(self, user_id: int, session: AsyncSession) -> Sequence[Conversation]:
        return await self.crud.get_all_by_filters(
            filters={"user_id": user_id}, session=session, order_by="created_at", descending=True
        )

    async def get_conversation_by_uuid(self, uuid: UUID, session: AsyncSession) -> Conversation:
        conversation: Conversation | None = await self.crud.get_by_uuid(uuid, session)

        if not conversation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No conversation found")

        return conversation

    async def create_conversation(
        self, title: str, user_id: int, session: AsyncSession, request: Request
    ) -> Conversation:
        try:
            headers_jwt: str = request.headers.get("Authorization", "")
            cookies_jwt: str = request.cookies.get(AuthCookieKey.ACCESS, "")

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8082/api/llm/title",
                    json={"model": "llama3.1:8b", "prompt": title},
                    headers={
                        "Authorization": headers_jwt if headers_jwt else f"Bearer {cookies_jwt}",
                        "X-LLM-Backend-Token": settings.LLM_SECRET_TOKEN,
                    },
                )

                if response.status_code == 403:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=response.json()["detail"],
                    )

                if response.status_code == 200:
                    data = response.json()

                    conversation: Conversation = Conversation(user_id=user_id, title=data.get("title", ""))
                    new_conversation = await self.crud.create(conversation, session)

                    await self.message_service.create_message(
                        conversation_uuid=new_conversation.uuid, content=title, role=Role.USER, session=session
                    )
                    return conversation
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="[Error] in generating conversation.",
                    )

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
