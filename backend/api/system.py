from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from core.config import settings

router = APIRouter(tags=["System"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_metadata() -> JSONResponse:
    content = {
        "name": "VitalMind Insight",
        "version": "0.1.0",
        "description": "AI-powered medical insights with LLM + OCR",
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> JSONResponse:
    content = {
        "status": "ok",
        "DB_USER": settings.DB_USER,
        "DB_PASSWORD": settings.DB_PASSWORD,
        "DB_HOST": settings.DB_HOST,
        "DB_NAME": settings.DB_NAME,
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)
