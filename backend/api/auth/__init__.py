from fastapi import APIRouter

from .auth import router as auth_router
from .web_auth import router as web_auth_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(web_auth_router, prefix="/web")
