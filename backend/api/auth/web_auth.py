from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.dependencies import services
from core.security import AuthCookieKey, AuthCookieManager
from db.session import get_session
from schemas.auth import AuthLogin, AuthRegister
from services import AuthService

router = APIRouter()


@router.post(
    "/register",
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

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Successfully registerd."})


@router.post(
    "/login",
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
    # AuthCookieManager.set_tokens(response=response, access_token=token.access_token, refresh_token=token.refresh_token)
    response.set_cookie(
        key=AuthCookieKey.ACCESS,
        value=token.access_token,
        httponly=False,
        secure=False,
        samesite="lax",
        max_age=settings.JWT_ACCESS_EXPIRE_MINUTES * 60 * 60,
    )

    response.set_cookie(
        key=AuthCookieKey.REFRESH,
        value=token.refresh_token,
        httponly=False,
        secure=False,
        samesite="lax",
        max_age=settings.JWT_REFRESH_EXPIRE_MINUTES * 60 * 60,
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Successfully logged in."})


@router.post("/logout", status_code=status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=2, minutes=1))])
async def web_logout(
    response: Response,
):
    AuthCookieManager.delete_token(response=response)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Successfully logged out."})
