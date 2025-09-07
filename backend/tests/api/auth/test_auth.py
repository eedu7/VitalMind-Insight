from typing import Any, Dict

import pytest
from httpx import AsyncClient

BASE_API_ENDPOINT: str = "/api/auth"

# -------------------------------
# Register Test
# -------------------------------


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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload_first, payload_second, expected_detail",
    [
        # Username conflict
        (
            {"email": "user1@example.com", "username": "sameuser", "password": "Password@123"},
            {"email": "user2@example.com", "username": "sameuser", "password": "Password@123"},
            "Username already exists",
        ),
        # Email conflict
        (
            {"email": "same@example.com", "username": "user1", "password": "Password@123"},
            {"email": "same@example.com", "username": "user2", "password": "Password@123"},
            "Email already exists",
        ),
        # Both conflict
        (
            {"email": "same@example.com", "username": "sameuser", "password": "Password@123"},
            {"email": "same@example.com", "username": "sameuser", "password": "Password@123"},
            "Username already exists",  # could also be "Email already exists" depending on service logic
        ),
    ],
)
async def test_register_user_conflicts(
    client: AsyncClient,
    payload_first: Dict[str, str],
    payload_second: Dict[str, str],
    expected_detail: str,
):
    # Create first user
    await client.post(f"{BASE_API_ENDPOINT}/register", json=payload_first)

    # Try second user with conflicts
    response = await client.post(f"{BASE_API_ENDPOINT}/register", json=payload_second)

    assert response.status_code == 400
    data = response.json()
    assert data["message"] == expected_detail


@pytest.mark.asyncio
async def test_register_rate_limit(client: AsyncClient):
    payload_first = {
        "email": "john.doe.first@example.com",
        "username": "john.doe.first",
        "password": "Password@123",
    }
    await client.post(f"{BASE_API_ENDPOINT}/register", json=payload_first)

    payload_second = {
        "email": "john.doe.second@example.com",
        "username": "john.doe.second",
        "password": "Password@123",
    }
    await client.post(f"{BASE_API_ENDPOINT}/register", json=payload_second)

    payload_third = {
        "email": "john.doe.third@example.com",
        "username": "john.doe.third",
        "password": "Password@123",
    }
    response = await client.post(f"{BASE_API_ENDPOINT}/register", json=payload_third)

    assert response.status_code == 429


# -------------------------------
# LOGIN TESTS
# -------------------------------


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, user_data: Dict[str, str]):
    await client.post(f"{BASE_API_ENDPOINT}/register", json=user_data)

    user_data.pop("username")
    response = await client.post(f"{BASE_API_ENDPOINT}/login", json=user_data)

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"password": "Password@123"},  # missing email
        {"email": "john.doe@example.com"},  # missing password
        {},  # all missing
    ],
)
async def test_login_user_missing_values(client: AsyncClient, payload: Dict[str, Any]):
    response = await client.post(f"{BASE_API_ENDPOINT}/login", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_user_not_found(client: AsyncClient):
    payload = {"email": "not.fount@example.com", "password": "Password@123"}
    response = await client.post(f"{BASE_API_ENDPOINT}/login", json=payload)

    assert response.status_code == 400
    assert response.json()["message"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_login_user_invalid_password(client: AsyncClient, user_data: Dict[str, str]):
    await client.post(f"{BASE_API_ENDPOINT}/register", json=user_data)
    user_data.pop("username")
    user_data["password"] = "Password"
    response = await client.post(f"{BASE_API_ENDPOINT}/login", json=user_data)

    assert response.status_code == 400
    assert response.json()["message"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_login_user_rate_limiting(client: AsyncClient, user_data: Dict[str, str]):
    user_data.pop("username")
    await client.post(f"{BASE_API_ENDPOINT}/login", json=user_data)
    await client.post(f"{BASE_API_ENDPOINT}/login", json=user_data)
    await client.post(f"{BASE_API_ENDPOINT}/login", json=user_data)
    await client.post(f"{BASE_API_ENDPOINT}/login", json=user_data)
    await client.post(f"{BASE_API_ENDPOINT}/login", json=user_data)
    response = await client.post(f"{BASE_API_ENDPOINT}/login", json=user_data)

    assert response.status_code == 429


# -------------------------------
# LOGIN TESTS
# -------------------------------


@pytest.mark.asyncio
async def test_logout_success(client: AsyncClient, auth_token: Dict[str, str]):
    response = await client.post(f"{BASE_API_ENDPOINT}/logout", json=auth_token)

    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Successfully logged out."


@pytest.mark.asyncio
async def test_logout_invalid_access_token(client: AsyncClient, auth_token: Dict[str, str]):
    auth_token["access_token"] = "INVALID_ACCESS_TOKEN"
    response = await client.post(f"{BASE_API_ENDPOINT}/logout", json=auth_token)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout_invalid_refresh_token(client: AsyncClient, auth_token: Dict[str, str]):
    auth_token["refresh_token"] = "INVALID_REFRESH_TOKEN"
    response = await client.post(f"{BASE_API_ENDPOINT}/logout", json=auth_token)

    assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"access_token": "ACCESS_TOKEN"},  # missing refresh token
        {"refresh_token": "REFRESH_TOKEN"},  # missing access token
        {},  # missing all values
    ],
)
async def test_logout_missing_values(client: AsyncClient, payload: Dict[str, str]):
    response = await client.post(f"{BASE_API_ENDPOINT}/logout", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_logout_rate_limiting(client: AsyncClient, auth_token: Dict[str, str]):
    await client.post(f"{BASE_API_ENDPOINT}/logout", json=auth_token)
    await client.post(f"{BASE_API_ENDPOINT}/logout", json=auth_token)
    response = await client.post(f"{BASE_API_ENDPOINT}/logout", json=auth_token)

    assert response.status_code == 429
