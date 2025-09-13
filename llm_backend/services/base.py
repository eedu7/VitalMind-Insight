from abc import ABC, abstractmethod
from typing import Any


class BaseService(ABC):
    @abstractmethod
    def generate_response(self, prompt: str, system: str, model: str, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def generate_stream_response(self, prompt: str, system: str, model: str, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def generate_title(self, prompt: str, model: str):
        raise NotImplementedError
