from typing import Any, Dict

import pytest
from httpx import AsyncClient

BASE_API_ENDPOINT: str = "/api/auth/web"

# -------------------------------
# REGISTER TESTS
# -------------------------------


@pytest.mark.asyncio
async def test_web_register_user_success(client: AsyncClient, user_data: Dict[str, str]):
    response = await client.post(f"{BASE_API_ENDPOINT}/register", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Successfully registerd."
    assert "access_token" in client.cookies
    assert "refresh_token" in client.cookies


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
async def test_web_register_user_missing_values(client: AsyncClient, payload: Dict[str, Any]):
    response = await client.post(f"{BASE_API_ENDPOINT}/register", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload_first, payload_second, expected_detail",
    [
        (
            {"email": "user1@example.com", "username": "sameuser", "password": "Password@123"},
            {"email": "user2@example.com", "username": "sameuser", "password": "Password@123"},
            "Username already exists",
        ),
        (
            {"email": "same@example.com", "username": "user1", "password": "Password@123"},
            {"email": "same@example.com", "username": "user2", "password": "Password@123"},
            "Email already exists",
        ),
        (
            {"email": "same@example.com", "username": "sameuser", "password": "Password@123"},
            {"email": "same@example.com", "username": "sameuser", "password": "Password@123"},
            "Username already exists",
        ),
    ],
)
async def test_web_register_user_conflicts(
    client: AsyncClient,
    payload_first: Dict[str, str],
    payload_second: Dict[str, str],
    expected_detail: str,
):
    await client.post(f"{BASE_API_ENDPOINT}/register", json=payload_first)

    response = await client.post(f"{BASE_API_ENDPOINT}/register", json=payload_second)

    assert response.status_code == 400
    assert response.json()["message"] == expected_detail


@pytest.mark.asyncio
async def test_web_register_rate_limit(client: AsyncClient):
    await client.post(
        f"{BASE_API_ENDPOINT}/register",
        json={"email": "john1@example.com", "username": "john1", "password": "Password@123"},
    )
    await client.post(
        f"{BASE_API_ENDPOINT}/register",
        json={"email": "john2@example.com", "username": "john2", "password": "Password@123"},
    )
    response = await client.post(
        f"{BASE_API_ENDPOINT}/register",
        json={"email": "john3@example.com", "username": "john3", "password": "Password@123"},
    )
    assert response.status_code == 429


# -------------------------------
# LOGIN TESTS
# -------------------------------


@pytest.mark.asyncio
async def test_web_login_success(client: AsyncClient, user_data: Dict[str, str]):
    await client.post(f"{BASE_API_ENDPOINT}/register", json=user_data)

    login_payload = {"email": user_data["email"], "password": user_data["password"]}
    response = await client.post(f"{BASE_API_ENDPOINT}/login", json=login_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Successfully logged in."
    assert "access_token" in client.cookies
    assert "refresh_token" in client.cookies


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"password": "Password@123"},  # missing email
        {"email": "john.doe@example.com"},  # missing password
        {},  # all missing
    ],
)
async def test_web_login_user_missing_values(client: AsyncClient, payload: Dict[str, Any]):
    response = await client.post(f"{BASE_API_ENDPOINT}/login", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_web_login_user_not_found(client: AsyncClient):
    payload = {"email": "notfound@example.com", "password": "Password@123"}
    response = await client.post(f"{BASE_API_ENDPOINT}/login", json=payload)

    assert response.status_code == 400
    assert response.json()["message"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_web_login_user_invalid_password(client: AsyncClient, user_data: Dict[str, str]):
    await client.post(f"{BASE_API_ENDPOINT}/register", json=user_data)

    bad_login = {"email": user_data["email"], "password": "WrongPassword"}
    response = await client.post(f"{BASE_API_ENDPOINT}/login", json=bad_login)

    assert response.status_code == 400
    assert response.json()["message"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_web_login_user_rate_limiting(client: AsyncClient, user_data: Dict[str, str]):
    login_payload = {"email": user_data["email"], "password": user_data["password"]}
    for _ in range(5):
        await client.post(f"{BASE_API_ENDPOINT}/login", json=login_payload)

    response = await client.post(f"{BASE_API_ENDPOINT}/login", json=login_payload)
    assert response.status_code == 429


# -------------------------------
# LOGOUT TESTS
# -------------------------------


@pytest.mark.asyncio
async def test_web_logout_success(client: AsyncClient, user_data: Dict[str, str]):
    # Register and login first
    await client.post(f"{BASE_API_ENDPOINT}/register", json=user_data)
    login_payload = {"email": user_data["email"], "password": user_data["password"]}
    await client.post(f"{BASE_API_ENDPOINT}/login", json=login_payload)

    # Logout
    response = await client.post(f"{BASE_API_ENDPOINT}/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out."
    assert "access_token" not in client.cookies
    assert "refresh_token" not in client.cookies


@pytest.mark.asyncio
async def test_web_logout_rate_limiting(client: AsyncClient, user_data: Dict[str, str]):
    await client.post(f"{BASE_API_ENDPOINT}/register", json=user_data)
    login_payload = {"email": user_data["email"], "password": user_data["password"]}
    await client.post(f"{BASE_API_ENDPOINT}/login", json=login_payload)

    await client.post(f"{BASE_API_ENDPOINT}/logout")
    await client.post(f"{BASE_API_ENDPOINT}/logout")
    response = await client.post(f"{BASE_API_ENDPOINT}/logout")

    assert response.status_code == 429
