from typing import Tuple

from fastapi.requests import HTTPConnection
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import AuthenticationMiddleware as BaseAuthenticationMiddleware

from core.security import jwt_handler
from schemas.user import CurrentUser


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> Tuple[bool, CurrentUser | None]:  # type: ignore
        current_user = CurrentUser(uuid=None)

        authorization: str | None = conn.headers.get("Authorization")

        if not authorization:
            return False, None

        try:
            scheme, token = authorization.split(" ")

            if scheme.lower() != "bearer":
                return False, None

        except ValueError:
            return False, None

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
