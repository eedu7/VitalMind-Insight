from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import AuthenticationRequired, get_current_active_user, services
from db import get_session
from db.models import User
from services import ConversationService

router = APIRouter(dependencies=[Depends(AuthenticationRequired)])


class ConversationCreate(BaseModel):
    title: str


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_conversation(
    data: ConversationCreate,
    current_user: User = Depends(get_current_active_user),
    conversation_service: ConversationService = Depends(services.get_conversation_service),
    session: AsyncSession = Depends(get_session),
):
    return await conversation_service.create_conversation(data.title, current_user.id, session)
