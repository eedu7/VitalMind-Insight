from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import BaseCRUD
from db.models import Conversation


class ConversationCRUD(BaseCRUD[Conversation]):
    def __init__(
        self,
    ) -> None:
        super().__init__(Conversation)

    async def create_conversation(self, title: str, user_id: int, session: AsyncSession) -> Conversation:
        try:
            conversation = Conversation(user_id=user_id, title=title)

            await self.create(conversation, session)

            return conversation
        except SQLAlchemyError as e:
            raise ValueError("Database error: {e}") from e
