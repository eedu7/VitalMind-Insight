from typing import Dict

import pytest
from httpx import AsyncClient

BASE_API_URL = "/api/user"

# -------------------------------
# GET User Profile
# -------------------------------


@pytest.mark.asyncio
async def test_user_profile_success(client: AsyncClient, auth_headers: Dict[str, str]):
    response = await client.get(f"{BASE_API_URL}/profile", headers=auth_headers)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_profile_no_headers(
    client: AsyncClient,
):
    response = await client.get(
        f"{BASE_API_URL}/profile",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_user_profile_rate_limiting(client: AsyncClient, auth_headers: Dict[str, str]):
    for _ in range(60):
        await client.get(f"{BASE_API_URL}/profile", headers=auth_headers)

    response = await client.get(f"{BASE_API_URL}/profile", headers=auth_headers)

    assert response.status_code == 429
