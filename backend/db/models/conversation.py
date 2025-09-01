from uuid import UUID

from sqlalchemy import UUID as PG_UUID
from sqlalchemy import ForeignKey, Unicode
from sqlalchemy.orm import Mapped, mapped_column

from db import Base
from db.mixins import PKUUIDMixin, TimeStampMixin


class Conversation(Base, TimeStampMixin, PKUUIDMixin):
    __tablename__ = "conversations"

    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(Unicode(255), nullable=False, index=True)
