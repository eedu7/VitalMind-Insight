from fastapi import APIRouter

from .health import router as health_router

router = APIRouter(prefix="/api")


__all__ = ["router", "health_router"]
