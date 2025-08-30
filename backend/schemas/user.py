from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserOut(BaseModel):
    uuid: UUID
    email: EmailStr
    username: str

    model_config = ConfigDict(from_attributes=True)


class CurrentUser(BaseModel):
    uuid: UUID | None = Field(
        None,
        description="Unique UUID identifier of the user.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
