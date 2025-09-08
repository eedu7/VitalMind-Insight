from typing import Literal

from services.llm.base import BaseLLMService
from services.llm.ollama_service import OllamaService

LLMType = Literal["ollama", "gemini"]


class LLMManager:
    def __init__(self, llm_type: LLMType = "ollama", model: str | None = None) -> None:
        self.llm_type = llm_type
        self.model = model
        self.llm = self._load_llm_service()

    def _load_llm_service(self) -> BaseLLMService:
        match self.llm_type:
            case "ollama":
                return OllamaService(model=self.model or "llama3.1:8b")
            case _:
                raise ValueError(f"Unsupported LLM type: {self.llm_type}")

    async def generate_title(self, prompt: str) -> str:
        prompt = f"Generate a short, concise conversation title (max 5 words) for this message:\n\n{prompt}"

        try:
            title = await self.llm.get_response(prompt)

            return title[1 : len(title) - 1]
        except Exception:
            words = prompt.strip().split()
            return " ".join(words[:7]).capitalize() if words else "New Conversation"

    def get_service(self) -> BaseLLMService:
        return self.llm
