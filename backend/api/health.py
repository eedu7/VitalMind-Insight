from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Health"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_metadata() -> JSONResponse:
    content = {
        "name": "VitalMind Insight",
        "version": "0.1.0",
        "description": "AI-powered medical insights with LLM + OCR",
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)
