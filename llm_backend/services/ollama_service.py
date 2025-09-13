import asyncio
import json

import httpx
from fastapi import HTTPException, status

from utils import format_response

from .base import BaseService


class OllamaService(BaseService):
    async def generate_response(self, prompt: str, system: str | None = None, model: str = "llama3.1:8b") -> str:
        try:
            messages = [{"role": "system", "content": "You are a helpful assistant."}]
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:11434/api/chat",
                    json={"model": model, "messages": messages, "stream": False},
                )
                response.raise_for_status()

                data = response.json()
                return data.get("message", {}).get("content", "")
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error in generating response: {exc}",
            )

    async def generate_stream_response(self, prompt: str, system: str | None = None, model: str = "llama3.1:8b"):
        try:
            messages = [{"role": "system", "content": "You are a helpful assistant."}]
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    "http://localhost:11434/api/chat",
                    json={"model": model, "messages": messages, "stream": True},
                ) as response:
                    response.raise_for_status()

                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue
                        try:
                            data = json.loads(line)
                            content = data.get("message", {}).get("content", "")
                            if content:
                                yield content
                                await asyncio.sleep(0)  # let event loop breathe
                        except json.JSONDecodeError:
                            continue

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error in generating streaming response: {exc}",
            )

    async def generate_title(self, prompt: str, model: str = "llama3.1:8b"):
        system: str = "Generate a short, concise title (max 4 words and no more than 38 characters) for this message"
        response = await self.generate_response(prompt, system=system, model=model)
        return format_response(response)
