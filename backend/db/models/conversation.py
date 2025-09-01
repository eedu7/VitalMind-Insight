from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlalchemy import UUID as PG_UUID
from sqlalchemy import ForeignKey, Unicode
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
from db.mixins import PKUUIDMixin, TimeStampMixin

# Forward reference for type hints. Import is skipped at runtime
# to prevent circular import issues between Message and Conversation.
if TYPE_CHECKING:
    from .message import Message


class Conversation(Base, TimeStampMixin, PKUUIDMixin):
    __tablename__: str = "conversations"

    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(Unicode(255), nullable=False, index=True)

    messages: Mapped[List["Message"]] = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphans", lazy="selectin"
    )
