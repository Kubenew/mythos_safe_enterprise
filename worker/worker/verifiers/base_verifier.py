from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseVerifier(ABC):
    """Base class for all verifiers."""
    
    @abstractmethod
    def verify(self, prompt: str, response: str, **kwargs) -> Dict[str, Any]:
        """
        Returns:
            {
                "reward": float [0.0, 1.0],
                "details": dict with metrics
            }
        """
        pass
    
    def __call__(self, prompt: str, response: str, **kwargs) -> Dict[str, Any]:
        return self.verify(prompt, response, **kwargs)
