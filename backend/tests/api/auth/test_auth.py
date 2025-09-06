from typing import Any, Dict

import pytest
from httpx import AsyncClient

BASE_API_ENDPOINT: str = "/api/auth"


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    payload = {"email": "john.doe@example.com", "username": "newuser", "password": "Password@123"}

    response = await client.post(f"{BASE_API_ENDPOINT}/register", json=payload)

    assert response.status_code == 201
    data: Dict[str, Any] = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"username": "newuser", "password": "Password@123"},  # missing email
        {"email": "john.doe@example.com", "password": "Password@123"},  # missing username
        {"email": "john.doe@example.com", "username": "newuser"},  # missing password
        {},  # all missing
    ],
)
async def test_register_user_missing_values(client: AsyncClient, payload: Dict[str, Any]):
    response = await client.post(f"{BASE_API_ENDPOINT}/register", json=payload)

    assert response.status_code == 422
