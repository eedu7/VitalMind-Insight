from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from db.models.message import Role


class Base(BaseModel):
    role: Role = Field(
        Role.USER,
        description="Role of the message sender (system, user, assistant, tool)",
        examples=[Role.USER],
    )
    content: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Content of the message",
        examples=["Hello, I need help with my account."],
    )


class MessageCreate(Base):
    conversation_uuid: UUID = Field(
        ...,
        description="Unique identifier of the conversation this message belongs to",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )


class MessageUpdate(Base):
    pass


class MessageOut(Base):
    uuid: UUID = Field(
        ...,
        description="Unique identifier of the message",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    model_config = ConfigDict(from_attributes=True)
