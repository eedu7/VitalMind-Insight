from uuid import UUID

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import BaseCRUD
from db.models import Message
from db.models.conversation import Conversation
from db.models.message import Role


class MessageCRUD(BaseCRUD[Message]):
    def __init__(
        self,
    ) -> None:
        super().__init__(Message)

    async def create_message(self, conversation_uuid: UUID, role: Role, content: str, session: AsyncSession) -> Message:
        stmt = (
            insert(Message)
            .values(
                conversation_id=select(Conversation.id).where(Conversation.uuid == conversation_uuid).scalar_subquery(),
                role=role,
                content=content,
            )
            .returning(Message)
        )

        result = await session.execute(stmt)
        await session.commit()
        return result.scalar_one()
