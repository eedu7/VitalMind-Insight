import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    payload = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "Password@123",
    }
    response = await client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_user(client: AsyncClient):
    payload = {"email": "dup@example.com", "username": "dupuser", "password": "Password@123"}
    await client.post("/api/auth/register", json=payload)
    response = await client.post("/api/auth/register", json=payload)
    assert response.status_code == 400 or response.status_code == 409


@pytest.mark.asyncio
async def test_register_invalid_email(client: AsyncClient):
    payload = {"email": "not-an-email", "username": "invaliduser", "password": "Password@123"}
    response = await client.post("/api/auth/register", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_weak_password(client: AsyncClient):
    payload = {"email": "weak@example.com", "username": "weakpass", "password": "123"}
    response = await client.post("/api/auth/register", json=payload)
    assert response.status_code == 400 or response.status_code == 422


@pytest.mark.asyncio
async def test_login_user_success(client: AsyncClient):
    payload = {"email": "login@example.com", "username": "loginuser", "password": "Password@123"}
    await client.post("/api/auth/register", json=payload)
    login_payload = {"email": "login@example.com", "password": "Password@123"}
    response = await client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    payload = {"email": "wrongpass@example.com", "username": "wronguser", "password": "Password@123"}
    await client.post("/api/auth/register", json=payload)
    login_payload = {"email": "wrongpass@example.com", "password": "WrongPassword"}
    response = await client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    payload = {"email": "ghost@example.com", "password": "Password@123"}
    response = await client.post("/api/auth/login", json=payload)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout_success(client: AsyncClient):
    payload = {"email": "logout@example.com", "username": "logoutuser", "password": "Password@123"}
    reg_res = await client.post("/api/auth/register", json=payload)
    tokens = reg_res.json()
    logout_payload = {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
    }
    response = await client.post("/api/auth/logout", json=logout_payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out."


@pytest.mark.asyncio
async def test_logout_with_invalid_token(client: AsyncClient):
    logout_payload = {"access_token": "fake_access", "refresh_token": "fake_refresh"}
    response = await client.post("/api/auth/logout", json=logout_payload)
    assert response.status_code == 401 or response.status_code == 400


@pytest.mark.asyncio
async def test_rate_limit_register(client: AsyncClient):
    payload = {"email": "ratelimit@example.com", "username": "ratelimit", "password": "Password@123"}
    for _ in range(2):
        await client.post("/api/auth/register", json=payload)
    response = await client.post("/api/auth/register", json=payload)
    assert response.status_code == 429
