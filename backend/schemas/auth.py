from pydantic import BaseModel, EmailStr, Field


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
class AuthRegister(Base):
    password: str = Field(
        ...,
        description="The account password. Must include uppercase, lowercase, numbers, and symbols.",
        examples=["Password@123", "SecurePass!456"],
    )


# For login
class AuthLogin(BaseModel):
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
class AuthOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
