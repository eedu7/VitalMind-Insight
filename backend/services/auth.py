from uuid import UUID

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.security import jwt_handler, token_blacklist
from core.security.blacklist import TokenBlacklist
from core.security.jwt_handler import JwtHandler
from core.security.password import Password
from crud import UserCRUD
from db.models import User
from schemas.auth import AuthOut


class AuthService:
    def __init__(self, crud: UserCRUD) -> None:
        self.crud = crud
        self.jwt_handler: JwtHandler = jwt_handler
        self.blacklist: TokenBlacklist = token_blacklist

    async def register(
        self, email: EmailStr, username: str, password: str, session: AsyncSession
    ) -> AuthOut:
        conflicts = await self.crud.check_user_exists(
            email=str(email), username=username, session=session
        )

        if conflicts["username"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )

        if conflicts["email"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

        # Hash password
        hashed_password = Password.hash_password(password)

        user = await self.crud.create_user(
            email=str(email),
            username=username,
            password=hashed_password,
            session=session,
        )

        return self._generate_token(user.uuid, user.username, user.email)

    async def login(self, email: EmailStr, password: str, session: AsyncSession) -> AuthOut:
        user: User | None = await self.crud.get_by_email(str(email), session)

        if not user or not Password.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
            )

        return self._generate_token(user.uuid, user.username, user.email)

    async def logout(self, access_token: str, refresh_token: str) -> None:
        access_payload = self.jwt_handler.decode(access_token, expected_type="access")
        refresh_payload = self.jwt_handler.decode(refresh_token, expected_type="refresh")

        if access_payload.get("sub") != refresh_payload.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access and refresh token do not match.",
            )

        await self.blacklist.add(access_payload)
        await self.blacklist.add(refresh_payload)

    def _generate_token(self, user_uuid: UUID, username: str, email: str) -> AuthOut:
        access_payload = {"sub": str(user_uuid), "username": username, "email": email}
        refresh_payload = {"sub": str(user_uuid)}

        access_token = self.jwt_handler.encode(
            access_payload,
            token_type="access",
            expire_minutes=settings.JWT_ACCESS_EXPIRE_MINUTES,
        )
        refresh_token = self.jwt_handler.encode(
            refresh_payload,
            token_type="refresh",
            expire_minutes=settings.JWT_REFRESH_EXPIRE_MINUTES,
        )

        return AuthOut(access_token=access_token, refresh_token=refresh_token)
