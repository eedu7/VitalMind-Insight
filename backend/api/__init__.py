from fastapi import APIRouter

from .system import router as system_router

router = APIRouter(prefix="/api")


__all__ = ["router", "system_router"]
