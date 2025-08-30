from fastapi import APIRouter, Depends

from core.dependencies import AuthenticationRequired, get_current_active_user
from db.models import User
from schemas.user import UserOut

router = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@router.get("/profile", response_model=UserOut)
async def profile(current_user: User = Depends(get_current_active_user)):
    return current_user
