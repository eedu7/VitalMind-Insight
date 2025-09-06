from typing import Any, Dict
from uuid import uuid4

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


@pytest.mark.asyncio
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


@pytest.mark.asyncio
async def test_get_conversation_by_uuid_success(client: AsyncClient, auth_headers: Dict[str, Any]):
    payload = {"title": "How was your day?"}
    response = await client.post(f"{BASE_API_ENDPOINT}/", json=payload, headers=auth_headers)

    conversation_uuid = response.json()["uuid"]

    response = await client.get(f"{BASE_API_ENDPOINT}/{conversation_uuid}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert "uuid" in data
    assert "title" in data


@pytest.mark.asyncio
async def test_get_conversation_by_uuid_not_found(client: AsyncClient, auth_headers: Dict[str, Any]):
    dummy_uuid = uuid4()

    response = await client.get(f"{BASE_API_ENDPOINT}/{dummy_uuid}", headers=auth_headers)

    assert response.status_code == 404


# -------------------------------
# UPDATE
# -------------------------------


@pytest.mark.asyncio
async def test_update_conversation_success(client: AsyncClient, auth_headers: Dict[str, Any]):
    payload = {"title": "How was your day?"}
    conversation_response = await client.post(f"{BASE_API_ENDPOINT}/", json=payload, headers=auth_headers)

    conversation_uuid = conversation_response.json()["uuid"]

    payload["title"] = "updated title"

    await client.put(f"{BASE_API_ENDPOINT}/{conversation_uuid}", json=payload, headers=auth_headers)

    response = await client.get(f"{BASE_API_ENDPOINT}/{conversation_uuid}", headers=auth_headers)

    assert response.status_code == 200

    assert response.json()["title"] == payload["title"]


@pytest.mark.asyncio
async def test_update_conversation_not_found(client: AsyncClient, auth_headers: Dict[str, Any]):
    payload = {"title": "How was your day?"}
    await client.post(f"{BASE_API_ENDPOINT}/", json=payload, headers=auth_headers)

    conversation_uuid = uuid4()

    payload["title"] = "updated title"

    response = await client.put(f"{BASE_API_ENDPOINT}/{conversation_uuid}", json=payload, headers=auth_headers)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_conversation_missing_title(client: AsyncClient, auth_headers: Dict[str, Any]):
    payload = {"title": "How was your day?"}
    await client.post(f"{BASE_API_ENDPOINT}/", json=payload, headers=auth_headers)

    conversation_uuid = uuid4()

    response = await client.put(f"{BASE_API_ENDPOINT}/{conversation_uuid}", headers=auth_headers)

    assert response.status_code == 422


# -------------------------------
# DELETE
# -------------------------------


@pytest.mark.asyncio
async def test_delete_conversation_success(client: AsyncClient, auth_headers: Dict[str, Any]):
    payload = {"title": "How was your day?"}
    conversation_response = await client.post(f"{BASE_API_ENDPOINT}/", json=payload, headers=auth_headers)

    conversation_uuid = conversation_response.json()["uuid"]

    response = await client.delete(f"{BASE_API_ENDPOINT}/{conversation_uuid}", headers=auth_headers)

    assert response.status_code == 200

    assert "message" in response.json()

    response = await client.get(f"{BASE_API_ENDPOINT}/{conversation_uuid}", headers=auth_headers)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_conversation_not_found(client: AsyncClient, auth_headers: Dict[str, Any]):
    conversation_uuid = uuid4()

    response = await client.delete(f"{BASE_API_ENDPOINT}/{conversation_uuid}", headers=auth_headers)

    assert response.status_code == 404
