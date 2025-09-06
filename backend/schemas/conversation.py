from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from schemas.message import MessageOut


class ConversationCreate(BaseModel):
    title: str = Field(
        ...,
        description="Title of the conversation",
        examples=["AI project brainstorming", "Medical chatbot session"],
    )


class ConversationDelete(BaseModel):
    conversation_uuid: UUID = Field(
        ...,
        description="Unique identifier of the conversation to delete",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )


class ConversationUpdate(ConversationCreate):
    pass


class ConversationOut(ConversationCreate):
    uuid: UUID = Field(
        ...,
        description="Unique identifier of the conversation.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    messages: List[MessageOut] = Field(
        ...,
        description="List of messages exchanged in the conversation",
    )

    model_config = ConfigDict(from_attributes=True)


class ConversationCreateOut(ConversationCreate):
    uuid: UUID = Field(
        ...,
        description="Unique identifier of the conversation.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )

    model_config = ConfigDict(from_attributes=True)
