from fastapi import APIRouter

from .health import router as health_router
from .llm import router as llm_router

router = APIRouter()


router.include_router(health_router, tags=["Health"])
router.include_router(llm_router, prefix="/api/llm", tags=["Large Language Model"])


router.get("/health")
