from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Shared base
class Base(BaseModel):
    email: EmailStr = Field(
        ...,
        description="The user's email address. Must be unique and valid.",
        examples=["john.doe@example.com"],
    )
    username: str = Field(
        ...,
        description="The display name chosen by the user. Must be unique.",
        examples=["JohnDoe", "Jane_Smith123"],
    )


# For registration
class UserCreate(Base):
    password: str = Field(
        ...,
        description="The account password. Must include uppercase, lowercase, numbers, and symbols.",
        examples=["Password@123", "SecurePass!456"],
    )


# For login
class UserLogin(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Registered email address used for login.",
        examples=["john.doe@example.com"],
    )
    password: str = Field(
        ...,
        description="Account password associated with the email.",
        examples=["Password@123"],
    )


# For API responses
class UserOut(Base):
    uuid: UUID = Field(
        ...,
        description="Unique UUID identifier of the user.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )

    model_config = ConfigDict(from_attributes=True)


class CurrentUser(BaseModel):
    uuid: UUID | None = Field(
        None,
        description="Unique UUID identifier of the user.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
