from abc import ABC, abstractmethod
from typing import Any


class BaseLLMService(ABC):
    @abstractmethod
    async def get_response(
        self,
        prompt: str | None = None,
        messages: list[dict[str, Any]] | None = None,
        model: str | None = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> Any:
        """
        Non-streaming response.
        - prompt: simple user message
        - messages: full chat messages [{"role": "user", "content": "..."}]
        - model: override model for this call
        - options: extra model parameters (temperature, top_p, etc.)
        """
        raise NotImplementedError

    @abstractmethod
    async def get_stream_response(
        self,
        prompt: str | None = None,
        messages: list[dict[str, Any]] | None = None,
        model: str | None = None,
        stream: bool = True,
        **kwargs: Any,
    ) -> Any:
        """
        Streaming response (yields chunks).
        Same params as get_response.
        """
        raise NotImplementedError
