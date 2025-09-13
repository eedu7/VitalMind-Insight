from typing import Any

from services.ollama_service import OllamaService


class LLMService:
    @classmethod
    def from_model(cls, model: str, **kwargs: Any):
        model_lower = model.lower()

        match model_lower:
            case "llama3.1:8b":
                return OllamaService(**kwargs)

            case _:
                raise ValueError(f"Unsupported model: {model}")
