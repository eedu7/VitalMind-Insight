from typing import List
from uuid import UUID

from pydantic import BaseModel

from schemas.message import MessageOut


class ConversationCreate(BaseModel):
    title: str


class ConversationOut(BaseModel):
    uuid: UUID
    title: str
    messages: List[MessageOut]
