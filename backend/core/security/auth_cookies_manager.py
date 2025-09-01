from enum import StrEnum
from typing import Dict

from fastapi import Request, Response

from core.config import TYPE_COOKIE_SAMESITE, settings


class AuthCookieKey(StrEnum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


class AuthCookieManager:
    _httponly: bool = settings.COOKIE_HTTPONLY
    _secure: bool = settings.COOKIE_SECURE
    _samesite: TYPE_COOKIE_SAMESITE = settings.COOKIE_SAMESITE

    @classmethod
    def set_tokens(cls, response: Response, access_token: str, refresh_token: str) -> None:
        cls._set(
            response=response,
            key=AuthCookieKey.ACCESS,
            value=access_token,
            max_age=settings.JWT_ACCESS_EXPIRE_MINUTES * 60,
            expires=settings.JWT_ACCESS_EXPIRE_MINUTES * 60,
        )
        cls._set(
            response=response,
            key=AuthCookieKey.REFRESH,
            value=refresh_token,
            max_age=settings.JWT_ACCESS_EXPIRE_MINUTES * 60,
            expires=settings.JWT_ACCESS_EXPIRE_MINUTES * 60,
        )

    @classmethod
    def delete_token(cls, response: Response) -> None:
        cls._delete(response=response, key=AuthCookieKey.ACCESS)
        cls._delete(response=response, key=AuthCookieKey.REFRESH)

    @classmethod
    def get_token(cls, request: Request) -> Dict[str, str | None]:
        return {
            "access_token": request.cookies.get(AuthCookieKey.ACCESS),
            "refresh_token": request.cookies.get(AuthCookieKey.REFRESH),
        }

    @classmethod
    def _set(cls, response: Response, key: str, value: str, max_age: int, expires: int) -> None:
        response.set_cookie(
            key=key,
            value=value,
            httponly=cls._httponly,
            secure=cls._secure,
            samesite=cls._samesite,
            max_age=max_age,
            expires=expires,
            path="/",
        )

    @classmethod
    def _delete(cls, response: Response, key: str) -> None:
        response.delete_cookie(key=key, httponly=cls._httponly, secure=cls._secure, samesite=cls._samesite)
