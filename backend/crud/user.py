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
