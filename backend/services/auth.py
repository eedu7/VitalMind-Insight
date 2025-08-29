from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from core.security.password import Password
from crud import UserCRUD


class AuthService:
    def __init__(self, crud: UserCRUD) -> None:
        self.crud = crud

    async def register(self, email: EmailStr, username: str, password: str, session: AsyncSession):
        conflicts = await self.crud.check_user_exists(email=str(email), username=username, session=session)

        if conflicts["username"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

        if conflicts["email"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

        # Hash password
        hashed_password = Password.hash_password(password)

        await self.crud.create_user(email=str(email), username=username, password=hashed_password, session=session)
