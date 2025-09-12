import asyncio
from typing import Dict

import httpx
from fastapi import HTTPException, status


class OllamaService:
    async def generate_response(
        self, prompt: str, system_role: Dict[str, str] | None = None, model: str = "llama3.1:8b"
    ) -> str:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:11434/api/chat",
                    json={
                        "model": "llama3.1:8b",
                        "messages": [
                            {"role": "system", "content": "You are a helpful assistant."},
                            system_role,
                            {"role": "user", "content": prompt},
                        ],
                        "stream": False,
                    },
                )
                response.raise_for_status()

                data = response.json()
                return data.get("message", {}).get("content", "")
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error in generating response: {exc}",
            )

    async def generate_stream_response(
        self, prompt: str, system_role: Dict[str, str] | None = None, model: str = "llama3.1:8b"
    ):
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    "http://localhost:11434/api/chat",
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": "You are a helpful assistant."},
                            system_role,
                            {"role": "user", "content": prompt},
                        ],
                    },
                ) as response:
                    response.raise_for_status()

                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue
                        try:
                            data = httpx.Response(status_code=status.HTTP_200_OK, content=line).json()
                            content = data.get("message", {}).get("content", {})

                            if content:
                                yield content
                                await asyncio.sleep(0)
                        except Exception:
                            continue

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error in generating streaming respnose: {exc}"
            )

    async def generate_title(self, prompt: str, model: str = "llama3.1:8b"):
        system_role = {
            "role": "system",
            "content": "Generate a short, concise title (max 4 words and no more than 38 characters) for this message",
        }

        return await self.generate_response(prompt, system_role=system_role, model=model)
