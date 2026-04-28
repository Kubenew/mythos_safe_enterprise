from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseVerifier(ABC):
    """Base class for all cyber defensive verifiers."""
    
    @abstractmethod
    def verify(self, prompt: str, response: str, **kwargs) -> Dict[str, Any]:
        """Returns reward and details dict."""
        pass
    
    def __call__(self, prompt: str, response: str, **kwargs) -> Dict[str, Any]:
        return self.verify(prompt, response, **kwargs)
