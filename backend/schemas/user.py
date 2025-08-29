from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Base(BaseModel):
    email: EmailStr = Field(..., description="Email", examples=["john.doe@example.com"])
    username: str = Field(..., description="Username", examples=["John Doe"])


class UserCreate(Base):
    password: str = Field(..., description="Password", examples=["Password@123"])


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(Base):
    id: int

    model_config = ConfigDict(from_attributes=True)
