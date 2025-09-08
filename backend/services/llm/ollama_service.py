from collections.abc import AsyncGenerator
from typing import Any, Dict, List

import httpx

from services.llm.base import BaseLLMService


class OllamaService(BaseLLMService):
    def __init__(self, model: str = "llama3.1:8b") -> None:
        self.model: str = model
        self.base_url: str = "http://localhost:11434/api/chat"

    async def get_response(
        self,
        prompt: str | None = None,
        messages: List[Dict[str, Any]] | None = None,
        model: str | None = None,
        stream: bool = False,
        **options: Any,
    ) -> str:
        payload: Dict[str, Any] = {
            "model": model or self.model,
            "messages": messages or [{"role": "user", "content": prompt}],
            "stream": stream,
            **options,
        }

        async with httpx.AsyncClient() as client:
            res = await client.post(self.base_url, json=payload)
            res.raise_for_status()
            data: Dict[str, Any] = res.json()
            return data.get("message", {}).get("content")

    async def get_stream_response(
        self,
        prompt: str | None = None,
        messages: List[Dict[str, Any]] | None = None,
        model: str | None = None,
        stream: bool = False,
        **options: Any,
    ) -> AsyncGenerator[str, None]:
        payload: Dict[str, Any] = {
            "model": model or self.model,
            "messages": messages or [{"role": "user", "content": prompt}],
            "stream": stream,
            **options,
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(self.base_url, json=payload)
            res.raise_for_status()
            data: Dict[str, Any] = res.json()
            return data.get("message", {}).get("content")
