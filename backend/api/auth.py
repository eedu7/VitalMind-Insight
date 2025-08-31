from fastapi import APIRouter, Depends, Response, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import services
from core.security import AuthCookieManager
from db.session import get_session
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


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(RateLimiter(times=2, minutes=1))])
async def logout(
    data: AuthLogOut,
    auth_service: AuthService = Depends(services.get_auth_service),
):
    await auth_service.logout(access_token=data.access_token, refresh_token=data.refresh_token)


@router.post(
    "/web/register",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RateLimiter(times=2, minutes=1))],
)
async def webstie_register(
    data: AuthRegister,
    response: Response,
    auth_service: AuthService = Depends(services.get_auth_service),
    session: AsyncSession = Depends(get_session),
):
    token = await auth_service.register(
        email=data.email,
        username=data.username,
        password=data.password,
        session=session,
    )

    AuthCookieManager.set_tokens(response=response, access_token=token.access_token, refresh_token=token.refresh_token)


@router.post(
    "/web/login",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(RateLimiter(times=5, minutes=1))],
)
async def web_login(
    data: AuthLogin,
    response: Response,
    auth_service: AuthService = Depends(services.get_auth_service),
    session: AsyncSession = Depends(get_session),
):
    token = await auth_service.login(email=data.email, password=data.password, session=session)
    AuthCookieManager.set_tokens(response=response, access_token=token.access_token, refresh_token=token.refresh_token)


@router.post(
    "/web/logout", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(RateLimiter(times=2, minutes=1))]
)
async def web_logout(
    response: Response,
):
    AuthCookieManager.delete_token(response=response)
