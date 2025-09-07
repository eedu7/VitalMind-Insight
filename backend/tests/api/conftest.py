from typing import Dict
from uuid import UUID, uuid4

import pytest
from faker import Faker
from httpx import AsyncClient

from core.config import settings
from core.security import jwt_handler

fake = Faker()


@pytest.fixture(scope="function")
def user_data() -> Dict[str, str]:
    return {
        "username": fake.user_name(),
        "email": fake.unique.email(),
        "password": fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True),
    }


@pytest.fixture(scope="function")
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


@pytest.fixture(scope="function")
async def auth_headers(client: AsyncClient, user_data: Dict[str, str]) -> Dict[str, str]:
    response = await client.post("/api/auth/register", json=user_data)
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


@pytest.fixture(scope="function")
async def conversation_uuid(client: AsyncClient, auth_headers: Dict[str, str]) -> str:
    response = await client.post("/api/conversation/", json={"title": "Test conversation"}, headers=auth_headers)
    return response.json()["uuid"]


@pytest.fixture(scope="function")
def message_payload(conversation_uuid: str) -> Dict[str, str]:
    return {"role": "user", "content": "Hello, I need help with my account.", "conversation_uuid": conversation_uuid}
