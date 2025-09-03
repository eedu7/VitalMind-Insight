from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import AuthenticationRequired, get_current_active_user, services
from db import get_session
from db.models import User
from schemas.conversation import ConversationCreate, ConversationDelete, ConversationOut, ConversationUpdate
from services import ConversationService

router = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ConversationOut)
async def create_conversation(
    data: ConversationCreate,
    current_user: User = Depends(get_current_active_user),
    conversation_service: ConversationService = Depends(services.get_conversation_service),
    session: AsyncSession = Depends(get_session),
):
    return await conversation_service.create_conversation(data.title, current_user.id, session)


@router.put("/", status_code=status.HTTP_200_OK)
async def update_conversation(
    data: ConversationUpdate,
    conversation_service: ConversationService = Depends(services.get_conversation_service),
    session: AsyncSession = Depends(get_session),
):
    await conversation_service.update_conversation(data.conversation_uuid, data.title, session)
    return {"message": "Conversation updated."}


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_conversation(
    data: ConversationDelete,
    conversation_service: ConversationService = Depends(services.get_conversation_service),
    session: AsyncSession = Depends(get_session),
):
    await conversation_service.delete_conversation(data.conversation_uuid, session)

    return {"message": "Conversation deleted."}
