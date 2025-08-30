from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import UserCRUD
from db.session import get_session
from schemas.auth import AuthLogin, AuthOut, AuthRegister
from services.auth import AuthService

router = APIRouter()

# Initialize CRUD and AuthService
crud = UserCRUD()
auth = AuthService(crud)


@router.post("/register", response_model=AuthOut)
async def register(data: AuthRegister, session: AsyncSession = Depends(get_session)):
    return await auth.register(
        email=data.email,
        username=data.username,
        password=data.password,
        session=session,
    )


@router.post("/login", response_model=AuthOut)
async def login(data: AuthLogin, session: AsyncSession = Depends(get_session)):
    return await auth.login(email=data.email, password=data.password, session=session)
