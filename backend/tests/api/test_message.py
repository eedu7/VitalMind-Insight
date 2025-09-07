from typing import Dict, List
from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient

BASE_API_ENDPOINT: str = "/api/message"


# -------------------------------
# CREATE
# -------------------------------


@pytest.mark.asyncio
async def test_create_message_success(
    client: AsyncClient, auth_headers: Dict[str, str], message_payload: Dict[str, str]
):
    response = await client.post(
        f"{BASE_API_ENDPOINT}/", json=message_payload, headers=auth_headers
    )

    assert response.status_code == 201

    data = response.json()

    assert "role" in data
    assert "content" in data
    assert "uuid" in data


@pytest.mark.asyncio
async def test_create_message_missing_fields(
    client: AsyncClient, auth_headers: Dict[str, str], message_payload: Dict[str, str]
):
    message_payload.pop("conversation_uuid")
    response = await client.post(
        f"{BASE_API_ENDPOINT}/", json=message_payload, headers=auth_headers
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_message_missing_header(client: AsyncClient, message_payload: Dict[str, str]):
    message_payload.pop("conversation_uuid")
    response = await client.post(f"{BASE_API_ENDPOINT}/", json=message_payload)

    assert response.status_code == 401


# -------------------------------
# GET SINGLE MESSAGE
# -------------------------------


@pytest.mark.asyncio
async def test_get_message_by_uuid_success(
    client: AsyncClient, auth_headers: Dict[str, str], message_payload: Dict[str, str]
):
    response = await client.post(
        f"{BASE_API_ENDPOINT}/", json=message_payload, headers=auth_headers
    )

    message_uuid = response.json()["uuid"]

    response = await client.get(f"{BASE_API_ENDPOINT}/{message_uuid}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert "uuid" in data
    assert "role" in data
    assert "content" in data


@pytest.mark.asyncio
async def test_get_message_by_uuid_not_found(
    client: AsyncClient,
    auth_headers: Dict[str, str],
):
    message_uuid: UUID = uuid4()
    response = await client.get(f"{BASE_API_ENDPOINT}/{message_uuid}", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_message_missing_header(client: AsyncClient, message_payload: Dict[str, str]):
    message_uuid = uuid4()
    response = await client.get(
        f"{BASE_API_ENDPOINT}/{message_uuid}",
    )
    assert response.status_code == 401


# -------------------------------
# GET MESSAGES BY CONVERSATION
# -------------------------------


# API ENDPOINT is api/message/all/{conversation_uuidz}
@pytest.mark.asyncio
async def test_get_messages_by_conversation_success(
    client: AsyncClient,
    message_payload: Dict[str, str],
    auth_headers: Dict[str, str],
    conversation_uuid: str,
):
    await client.post(f"{BASE_API_ENDPOINT}/", json=message_payload, headers=auth_headers)

    response = await client.get(
        f"{BASE_API_ENDPOINT}/all/{conversation_uuid}", headers=auth_headers
    )

    assert response.status_code == 200
    data: List[Dict[str, str]] = response.json()

    assert isinstance(data, list)
    assert len(data) == 1


@pytest.mark.asyncio
async def test_get_messages_by_conversation_missing_header(
    client: AsyncClient, conversation_uuid: str
):
    response = await client.get(
        f"{BASE_API_ENDPOINT}/all/{conversation_uuid}",
    )

    assert response.status_code == 401


# -------------------------------
# UPDATE
# -------------------------------


@pytest.mark.asyncio
async def test_update_message_success(
    client: AsyncClient, message_payload: Dict[str, str], auth_headers: Dict[str, str]
):
    response = await client.post(
        f"{BASE_API_ENDPOINT}/", json=message_payload, headers=auth_headers
    )

    updated_payload = {
        "role": "system",
        "content": "I'm system",
    }

    message_uuid = response.json()["uuid"]

    response = await client.put(
        f"{BASE_API_ENDPOINT}/{message_uuid}", json=updated_payload, headers=auth_headers
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_message_no_headers(
    client: AsyncClient, message_payload: Dict[str, str], auth_headers: Dict[str, str]
):
    response = await client.post(
        f"{BASE_API_ENDPOINT}/", json=message_payload, headers=auth_headers
    )

    updated_payload = {
        "role": "system",
        "content": "I'm system",
    }

    message_uuid = response.json()["uuid"]

    response = await client.put(f"{BASE_API_ENDPOINT}/{message_uuid}", json=updated_payload)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_message_not_found(client: AsyncClient, auth_headers: Dict[str, str]):
    message_uuid = uuid4()
    updated_payload = {
        "role": "system",
        "content": "I'm system",
    }

    response = await client.put(
        f"{BASE_API_ENDPOINT}/{message_uuid}", json=updated_payload, headers=auth_headers
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_message_missing_fields(client: AsyncClient, auth_headers: Dict[str, str]):
    message_uuid = uuid4()
    updated_payload: Dict[str, str] = {}

    response = await client.put(
        f"{BASE_API_ENDPOINT}/{message_uuid}", json=updated_payload, headers=auth_headers
    )

    assert response.status_code == 422


# -------------------------------
# DELETE
# -------------------------------


@pytest.mark.asyncio
async def test_delete_message_success(
    client: AsyncClient, message_payload: Dict[str, str], auth_headers: Dict[str, str]
):
    response = await client.post(
        f"{BASE_API_ENDPOINT}/", json=message_payload, headers=auth_headers
    )

    message_uuid = response.json()["uuid"]

    response = await client.delete(f"{BASE_API_ENDPOINT}/{message_uuid}", headers=auth_headers)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_message_not_found(client: AsyncClient, auth_headers: Dict[str, str]):
    message_uuid = uuid4()
    response = await client.delete(f"{BASE_API_ENDPOINT}/{message_uuid}", headers=auth_headers)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_message_no_headers(
    client: AsyncClient, message_payload: Dict[str, str], auth_headers: Dict[str, str]
):
    response = await client.post(
        f"{BASE_API_ENDPOINT}/", json=message_payload, headers=auth_headers
    )

    message_uuid = response.json()["uuid"]

    response = await client.delete(f"{BASE_API_ENDPOINT}/{message_uuid}")

    assert response.status_code == 401
