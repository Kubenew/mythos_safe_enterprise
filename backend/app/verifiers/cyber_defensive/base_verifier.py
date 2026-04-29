from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseVerifier(ABC):
    @abstractmethod
    def verify(self, prompt: str, response: str, **kwargs) -> Dict[str, Any]:
        pass

    def __call__(self, prompt: str, response: str, **kwargs) -> Dict[str, Any]:
        return self.verify(prompt, response, **kwargs)
