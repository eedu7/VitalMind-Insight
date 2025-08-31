from typing import Dict

from fastapi import Request, Response

from core.config import settings


class CookieManager:
    _ACCESS_TOKEN_KEY: str = "access_token"
    _REFRESH_TOKEN_KEY: str = "refresh_token"

    @classmethod
    def set_tokens(cls, response: Response, access_token: str, refresh_token: str) -> None:
        response.set_cookie(
            key=cls._ACCESS_TOKEN_KEY,
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=settings.JWT_ACCESS_EXPIRE_MINUTES,
        )

        response.set_cookie(
            key=cls._REFRESH_TOKEN_KEY,
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=settings.JWT_REFRESH_EXPIRE_MINUTES,
        )

    @classmethod
    def delete_token(cls, response: Response) -> None:
        response.delete_cookie(key=cls._ACCESS_TOKEN_KEY, httponly=True, secure=True, samesite="strict")
        response.delete_cookie(key=cls._REFRESH_TOKEN_KEY, httponly=True, secure=True, samesite="strict")

    @classmethod
    def get_token(cls, request: Request) -> Dict[str, str | None]:
        return {
            "access_token": request.cookies.get(cls._ACCESS_TOKEN_KEY),
            "refresh_token": request.cookies.get(cls._REFRESH_TOKEN_KEY),
        }
