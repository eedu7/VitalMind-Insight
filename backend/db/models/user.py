from sqlalchemy import Unicode
from sqlalchemy.orm import Mapped, mapped_column

from db import Base
from db.mixins import PKUUIDMixin, TimeStampMixin


class User(PKUUIDMixin, Base, TimeStampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(Unicode(255), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(Unicode(255), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(Unicode(255), nullable=False)

    def __repr__(self) -> str:
        return f"<User  id={self.id} uuid={self.uuid} username={self.username}>"
