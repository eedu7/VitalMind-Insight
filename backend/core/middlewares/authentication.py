from typing import Tuple

from fastapi import Request
from fastapi.requests import HTTPConnection
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import AuthenticationMiddleware as BaseAuthenticationMiddleware

from core.security import jwt_handler
from schemas.user import CurrentUser
from utils import CookieManager


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> Tuple[bool, CurrentUser | None]:  # type: ignore
        current_user = CurrentUser(uuid=None)

        authorization: str | None = conn.headers.get("Authorization")
        token: str | None = None
        if authorization:
            try:
                scheme, token = authorization.split(" ")

                if scheme.lower() != "bearer":
                    token = None

            except ValueError:
                token = None

        if not token and isinstance(conn, Request):
            tokens = CookieManager.get_token(conn)
            token = tokens.get("access_token")

        if not token:
            return False, None

        payload = jwt_handler.decode(token, expected_type="access")
        user_id = payload.get("sub", None)

        if user_id:
            current_user.uuid = user_id
            return True, current_user

        return False, None


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
