from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import UserCRUD
from db.session import get_session
from schemas.user import UserCreate, UserOut
from services.auth import AuthService

router = APIRouter()

# Initialize CRUD and AuthService
crud = UserCRUD()
auth = AuthService(crud)


@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await auth.register(
        email=user.email,
        username=user.username,
        password=user.password,
        session=session,
    )
