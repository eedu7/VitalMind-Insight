from uuid import UUID

from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    uuid: UUID | None = Field(
        None,
        description="Unique UUID identifier of the user.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
