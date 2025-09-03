from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from schemas.message import MessageOut


class ConversationCreate(BaseModel):
    title: str


class ConversationOut(BaseModel):
    uuid: UUID
    title: str
    messages: List[MessageOut]

    model_config = ConfigDict(from_attributes=True)


class ConversationDelete(BaseModel):
    conversation_uuid: UUID
