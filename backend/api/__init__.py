from fastapi import APIRouter

from .auth import router as auth_router
from .health import router as health_router
from .user import router as user_router

router = APIRouter(prefix="/api")

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(user_router, prefix="/user", tags=["User"])

__all__ = ["router", "health_router"]
