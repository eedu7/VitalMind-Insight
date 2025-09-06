from typing import Any, Dict

import pytest
from httpx import AsyncClient

BASE_API_ENDPOINT: str = "/api/conversation"


# -------------------------------
# CREATE
# -------------------------------


@pytest.mark.asyncio
async def test_create_conversation_success(client: AsyncClient, auth_headers: Dict[str, Any]):
    payload = {"title": "How was your day?"}
    response = await client.post(f"{BASE_API_ENDPOINT}/", json=payload, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert "uuid" in data
    assert "title" in data
    assert data["title"] == payload["title"]


@pytest.mark.asyncio
async def test_create_conversation_missing_title(client: AsyncClient, auth_headers: Dict[str, Any]):
    response = await client.post(f"{BASE_API_ENDPOINT}/", json={}, headers=auth_headers)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_missing_header(
    client: AsyncClient,
):
    payload = {"title": "How was your day?"}
    response = await client.post(
        f"{BASE_API_ENDPOINT}/",
        json=payload,
    )

    assert response.status_code == 401


# -------------------------------
# GET ALL
# -------------------------------


@pytest.mark.asyncio
async def test_get_all_conversations_success(client: AsyncClient, auth_headers: Dict[str, Any]):
    response = await client.get(f"{BASE_API_ENDPOINT}/", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)


@pytest.mark.skip
async def test_get_all_conversation_no_header(
    client: AsyncClient,
):
    response = await client.get(
        f"{BASE_API_ENDPOINT}/",
    )

    assert response.status_code == 401


# -------------------------------
# GET BY UUID
# -------------------------------


@pytest.mark.skip
async def test_get_conversation_by_uuid_success(client: AsyncClient, auth_headers: Dict[str, Any]):
    raise NotImplementedError


@pytest.mark.skip
async def test_get_conversation_by_uuid_not_found(client: AsyncClient, auth_headers: Dict[str, Any]):
    raise NotImplementedError


# -------------------------------
# UPDATE
# -------------------------------


@pytest.mark.skip
async def test_update_conversation_success(client: AsyncClient, auth_headers: Dict[str, Any]):
    raise NotImplementedError


@pytest.mark.skip
async def test_update_conversation_not_found(client: AsyncClient, auth_headers: Dict[str, Any]):
    raise NotImplementedError


@pytest.mark.skip
async def test_update_conversation_missing_title(client: AsyncClient, auth_headers: Dict[str, Any]):
    raise NotImplementedError


# -------------------------------
# DELETE
# -------------------------------


@pytest.mark.skip
async def test_delete_conversation_success(client: AsyncClient, auth_headers: Dict[str, Any]):
    raise NotImplementedError


@pytest.mark.skip
async def test_delete_conversation_not_found(client: AsyncClient, auth_headers: Dict[str, Any]):
    raise NotImplementedError


# -------------------------------
# RATE LIMITING / EDGE CASES
# -------------------------------


@pytest.mark.skip
async def test_conversation_rate_limit(client: AsyncClient, auth_headers: Dict[str, Any]):
    raise NotImplementedError


@pytest.mark.skip
async def test_concurrent_conversation_creations(client: AsyncClient, auth_headers: Dict[str, Any]):
    raise NotImplementedError
