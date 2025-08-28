from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from db.session import get_session

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
async def health_check(session: AsyncSession = Depends(get_session)) -> JSONResponse:
    try:
        result = await session.execute(text("SELECT 'OK'"))
        db_status = result.scalar_one_or_none()
        content = {"status": "Good", "db": db_status or "Failed", "DB_HOST": settings.DB_HOST}
    except Exception as e:
        content = {"status": "Bad", "db": str(e), "config": settings.model_dump()}

    return JSONResponse(status_code=status.HTTP_200_OK, content=content)
