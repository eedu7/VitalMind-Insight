from fastapi import APIRouter

from .auth import router as auth_router
from .health import router as health_router

router = APIRouter(prefix="/api")

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])

__all__ = ["router", "health_router"]
