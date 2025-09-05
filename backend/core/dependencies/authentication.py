from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.exceptions import UnauthorizedException
from core.security import AuthCookieManager, jwt_handler, token_blacklist


class AuthenticationRequired:
    def __init__(
        self,
    ):
        self.http_bearer = HTTPBearer(auto_error=False)
        self.jwt_handler = jwt_handler
        self.token_blacklist = token_blacklist

    async def __call__(
        self,
        request: Request,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    ):
        access_token: str | None = token.credentials if token else None

        if not access_token:
            cookies = AuthCookieManager.get_token(request)
            access_token = cookies.get("access_token")

        if not access_token:
            raise UnauthorizedException("Authentication required")

        payload = self.jwt_handler.decode(access_token, expected_type="access")

        blacklisted = await self.token_blacklist.is_blacklisted(payload.get("jti", ""))
        if blacklisted:
            raise UnauthorizedException("Token has been revoked or logged out. Please authenticate again.")

        return payload
