from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from core.config import settings


class Authentication(BaseModel):
    secret_token: str


class AuthenticationRequired:
    def __init__(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
        x_lllm_backend_token: str | None = Header(default=None, alias="X-LLM-Backend-Token"),
    ) -> None:
        if not credentials:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication requried")

        if not x_lllm_backend_token or x_lllm_backend_token != settings.LLM_SECRET_TOKEN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid backend authentication token")
