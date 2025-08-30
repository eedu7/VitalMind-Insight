from fastapi import APIRouter, Depends, status
from fastapi_limiter.depends import RateLimiter

from core.dependencies import AuthenticationRequired, get_current_active_user
from db.models import User
from schemas.user import UserOut

router = APIRouter(dependencies=[Depends(AuthenticationRequired())])


@router.get(
    "/profile",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(RateLimiter(times=60, minutes=1))],
)
async def profile(current_user: User = Depends(get_current_active_user)):
    return current_user
