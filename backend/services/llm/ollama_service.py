import json
from typing import Any, Dict, List

import aiohttp

from services.llm.base import BaseLLMService


class OllamaService(BaseLLMService):
    def __init__(self, model: str = "llama3.1:8b"):
        self.model: str = model
        self.base_url: str = "http://localhost:11434/api/chat"

    async def get_response(
        self,
        prompt: str | None = None,
        messages: List[Dict[str, Any]] | None = None,
        model: str | None = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> str:
        payload: Dict[str, Any] = {
            "model": model or self.model,
            "messages": messages or [{"role": "user", "content": prompt}],
            "stream": stream,
            **kwargs,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.base_url,
                json=payload,
            ) as res:
                data = await res.json()
                return data.get("message", {}).get("content", "")

    async def stream_response(  # type: ignore
        self,
        prompt: str | None = None,
        messages: List[Dict[str, Any]] | None = None,
        model: str | None = None,
        stream: bool = True,
        **kwargs: Any,
    ):
        payload: Dict[str, Any] = {
            "model": model or self.model,
            "messages": messages or [{"role": "user", "content": prompt}],
            "stream": stream,
            **kwargs,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, json=payload) as res:
                async for line_bytes in res.content:
                    line = line_bytes.decode().strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        content = data.get("message", {}).get("content")
                        if content:
                            yield content
                    except Exception:
                        yield line
