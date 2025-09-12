from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from core.dependencies import AuthenticationRequired
from services.ollama_service import OllamaService

router = APIRouter(dependencies=[Depends(AuthenticationRequired)])


class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    output: str


@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    service = OllamaService()
    response = await service.generate_response(request.prompt)
    return ChatResponse(output=response)


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    service = OllamaService()
    return StreamingResponse(service.generate_stream_response(request.prompt), media_type="text/plain")


class TitleRequest(BaseModel):
    prompt: str
    model: str = Field("llama3.1:8b")


@router.post("/title")
async def generate_title(request: TitleRequest):
    service = OllamaService()
