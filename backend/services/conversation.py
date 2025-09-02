from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from crud.conversation import ConversationCRUD
from db.models import Conversation


class ConversationService:
    def __init__(self, crud: ConversationCRUD) -> None:
        self.crud = crud

    async def create_conversation(self, title: str, user_id: int, session: AsyncSession) -> Conversation:
        try:
            conversation: Conversation = Conversation(user_id=user_id, title=title)

            await self.crud.create(conversation, session)

            return conversation
        except SQLAlchemyError as e:
            raise ValueError("Database error: {e}") from e
