from uuid import UUID

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    uuid: UUID
    email: EmailStr
    username: str


async def current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication requried")

    bearer = credentials.credentials

    # TODO: use an .env varialbe for this endpoint, settings.MAIN_BACKEND_URL/api/user/profile
    # or we can also make the /api/user/profile an .env
    url = "http://localhost:8080/api/user/profile"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers={"Authorization": f"Bearer {bearer}"}, timeout=10.0)
    except httpx.RequestError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Unable to reach authentication service")

    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired user token")

    return User(**response.json())
