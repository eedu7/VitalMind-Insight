from typing import Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import BaseCRUD
from models import User


class UserCRUD(BaseCRUD[User]):
    def __init__(
        self,
    ) -> None:
        super().__init__(User)

    async def get_by_email(self, email: str, session: AsyncSession) -> User | None:
        return await self.get_by(field="email", value=email, session=session)

    async def check_user_exists(
        self, username: str, email: str, session: AsyncSession
    ) -> Dict[str, bool]:
        """
        Check if a username or email already exists in the database.

        Args:
            username (str): Username to check.
            email (str): Email to check.
            session (AsyncSession): SQLAlchemy async session.

        Returns:
            Dict[str, bool]: Dictionary indicating which fields already exist.
        """
        stmt = select(User.username.label("username"), User.email.label("email")).where(
            (User.username == username) | (User.email == email)
        )

        result = await session.execute(stmt)
        user = result.first()

        conflicts = {"username": False, "email": False}

        if user:
            conflicts["username"] = user.username == username
            conflicts["email"] = user.email == email
        return conflicts

    async def create_user(
        self, email: str, username: str, password: str, session: AsyncSession
    ) -> User:
        user: User = User(username=username, email=email, password=password)
        return await self.create(user, session)
