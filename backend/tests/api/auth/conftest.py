from typing import Dict
from uuid import UUID, uuid4

import pytest

from core.config import settings
from core.security import jwt_handler


@pytest.fixture
def user_data() -> Dict[str, str]:
    return {"username": "JohnDoe", "email": "john.doe@example.com", "password": "Password@123"}


@pytest.fixture
def auth_token(user_data: Dict[str, str]) -> Dict[str, str]:
    user_uuid: UUID = uuid4()
    access_payload = {"sub": str(user_uuid), "username": user_data["username"], "email": user_data["email"]}
    refresh_payload = {"sub": str(user_uuid)}

    access_token = jwt_handler.encode(
        access_payload,
        token_type="access",
        expire_minutes=settings.JWT_ACCESS_EXPIRE_MINUTES,
    )
    refresh_token = jwt_handler.encode(
        refresh_payload,
        token_type="refresh",
        expire_minutes=settings.JWT_REFRESH_EXPIRE_MINUTES,
    )

    return {"access_token": access_token, "refresh_token": refresh_token}
