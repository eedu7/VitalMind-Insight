from sqlalchemy import Integer, Unicode
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(Unicode(255), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(Unicode(255), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(Unicode(255), nullable=False)

    def __repr__(self) -> str:
        return f"<User  id={self.id} username={self.username}>"
