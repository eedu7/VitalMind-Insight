from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import UUID as PG_UUID
from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
from db.mixins import PKUUIDMixin, TimeStampMixin

# Forward reference for type hints. Import is skipped at runtime
# to prevent circular import issues between Message and Conversation.
if TYPE_CHECKING:
    from .conversation import Conversation


class Role(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Message(Base, PKUUIDMixin, TimeStampMixin):
    __tablename__: str = "messages"

    conversation_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE")
    )
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.USER)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")
