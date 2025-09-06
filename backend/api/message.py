from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import AuthenticationRequired, services
from db import get_session
from schemas.message import MessageCreate, MessageOut, MessageUpdate
from services import MessageService

router = APIRouter(dependencies=[Depends(AuthenticationRequired())])


@router.get("/{message_uuid}", response_model=MessageOut)
async def get_message_by_uuid(
    message_uuid: UUID,
    message_service: MessageService = Depends(services.get_message_service),
    session: AsyncSession = Depends(get_session),
):
    return await message_service.get_message_by_uuid(message_uuid, session)


@router.get("/all/{conversation_uuid}", response_model=List[MessageOut])
async def get_messages_by_conversation_uuid(
    conversation_uuid: UUID,
    message_service: MessageService = Depends(services.get_message_service),
    session: AsyncSession = Depends(get_session),
):
    return await message_service.get_messages_by_conversation_uuid(conversation_uuid, session)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MessageOut)
async def create_message(
    data: MessageCreate,
    message_service: MessageService = Depends(services.get_message_service),
    session: AsyncSession = Depends(get_session),
):
    return await message_service.create_message(
        conversation_uuid=data.conversation_uuid, content=data.content, role=data.role, session=session
    )


@router.put("/{message_uuid}")
async def update_message(
    message_uuid: UUID,
    data: MessageUpdate,
    message_service: MessageService = Depends(services.get_message_service),
    session: AsyncSession = Depends(get_session),
):
    await message_service.update_message(
        content=data.content, message_uuid=message_uuid, role=data.role, session=session
    )

    return {"message": "Message updated."}


@router.delete("/{message_uuid}")
async def delete_message(
    message_uuid: UUID,
    message_service: MessageService = Depends(services.get_message_service),
    session: AsyncSession = Depends(get_session),
):
    await message_service.delete_message(message_uuid, session)

    return {"message": "Message deleted."}
