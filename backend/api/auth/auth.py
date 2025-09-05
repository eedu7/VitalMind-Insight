from fastapi import APIRouter, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import services
from core.security import jwt_handler, token_blacklist
from db import get_session
from schemas.auth import AuthLogin, AuthLogOut, AuthOut, AuthRegister
from services import AuthService

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=AuthOut,
    dependencies=[Depends(RateLimiter(times=2, minutes=1))],
)
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


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=AuthOut,
    dependencies=[Depends(RateLimiter(times=5, minutes=1))],
)
async def login(
    data: AuthLogin,
    auth_service: AuthService = Depends(services.get_auth_service),
    session: AsyncSession = Depends(get_session),
):
    return await auth_service.login(email=data.email, password=data.password, session=session)


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(RateLimiter(times=2, minutes=1))],
)
async def logout(
    data: AuthLogOut,
):
    access_payload = jwt_handler.decode(data.access_token, expected_type="access")
    refresh_payload = jwt_handler.decode(data.refresh_token, expected_type="refresh")

    await token_blacklist.add(access_payload)
    await token_blacklist.add(refresh_payload)

    return {"message": "Successfully logged out."}
