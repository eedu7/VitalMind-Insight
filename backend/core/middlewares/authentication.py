from typing import Tuple

from fastapi.requests import HTTPConnection
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import AuthenticationMiddleware as BaseAuthenticationMiddleware

from core.security import AuthCookieKey, jwt_handler
from schemas.user import CurrentUser


# WARNING: If people are passing the token in headers and cookies, if the headers one is expired, or revoked,
# and the cookie one if valid, the authentication fails, as it does not check, if the token is presented
# in the headers
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
            except Exception:
                token = None

        if not token:
            token = conn.cookies.get(AuthCookieKey.ACCESS)

        if not token:
            return False, None
        try:
            payload = jwt_handler.decode(token, expected_type="access")
            user_id = payload.get("sub", None)
        except Exception:
            return False, None
        if user_id:
            current_user.uuid = user_id
            return True, current_user

        return False, None


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
