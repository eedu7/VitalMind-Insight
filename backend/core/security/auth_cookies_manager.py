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
        response.set_cookie(
            key=AuthCookieKey.ACCESS,
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=settings.JWT_ACCESS_EXPIRE_MINUTES,
        )

        response.set_cookie(
            key=AuthCookieKey.REFRESH,
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=settings.JWT_REFRESH_EXPIRE_MINUTES,
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
