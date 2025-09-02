from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, Unicode
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
from db.mixins import PKUUIDMixin, TimeStampMixin

# Forward reference for type hints. Import is skipped at runtime
# to prevent circular import issues between Message and Conversation.
if TYPE_CHECKING:
    from .message import Message


class Conversation(PKUUIDMixin, Base, TimeStampMixin):
    __tablename__: str = "conversations"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(Unicode(255), nullable=False, index=True)

    messages: Mapped[List["Message"]] = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan", lazy="selectin"
    )
