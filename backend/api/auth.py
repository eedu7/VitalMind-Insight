from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import services
from db.session import get_session
from schemas.auth import AuthLogin, AuthOut, AuthRegister
from services import AuthService

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=AuthOut)
async def register(
    data: AuthRegister,
    auth_service: AuthService = Depends(services.get_auth_service),
    session: AsyncSession = Depends(get_session),
):
    return await auth_service.register(
        email=data.email,
        username=data.username,
        password=data.password,
        session=session,
    )


@router.post("/login", status_code=status.HTTP_200_OK, response_model=AuthOut)
async def login(
    data: AuthLogin,
    auth_service: AuthService = Depends(services.get_auth_service),
    session: AsyncSession = Depends(get_session),
):
    return await auth_service.login(email=data.email, password=data.password, session=session)
