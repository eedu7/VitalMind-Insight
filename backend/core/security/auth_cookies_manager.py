from enum import StrEnum
from typing import Dict

from fastapi import Request, Response

from core.config import settings


class AuthCookieKey(StrEnum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


class AuthCookieManager:
    @classmethod
    def set_tokens(cls, response: Response, access_token: str, refresh_token: str) -> None:
        print("Setting up cookies")
        response.set_cookie(
            key=AuthCookieKey.ACCESS,
            value=access_token,
            httponly=False,
            secure=False,
            samesite="lax",
            max_age=settings.JWT_ACCESS_EXPIRE_MINUTES * 60,
            path="/",
        )

        response.set_cookie(
            key=AuthCookieKey.REFRESH,
            value=refresh_token,
            httponly=False,
            secure=False,
            samesite="lax",
            max_age=settings.JWT_REFRESH_EXPIRE_MINUTES * 60,
            path="/",
        )

    @classmethod
    def delete_token(cls, response: Response) -> None:
        response.delete_cookie(key=AuthCookieKey.ACCESS, httponly=True, secure=True, samesite="strict")
        response.delete_cookie(key=AuthCookieKey.REFRESH, httponly=True, secure=True, samesite="strict")

    @classmethod
    def get_token(cls, request: Request) -> Dict[str, str | None]:
        return {
            "access_token": request.cookies.get(AuthCookieKey.ACCESS),
            "refresh_token": request.cookies.get(AuthCookieKey.REFRESH),
        }
