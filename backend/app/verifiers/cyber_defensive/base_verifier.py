"""
Base verifier module for Mythos Safe Enterprise.

This module defines the abstract base class for all verifiers used in the
cyber defensive evaluation pipeline.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseVerifier(ABC):
    """
    Abstract base class for all Mythos++ verifiers.
    
    All verifiers must implement the `verify` method which evaluates
    model responses and returns a reward score with details.
    
    Attributes:
        verify: Abstract method that must be implemented by subclasses.
        __call__: Convenience method to call verify directly.
    """

    @abstractmethod
    def verify(self, prompt: str, response: str, **kwargs) -> Dict[str, Any]:
        """
        Verify a model response against the prompt and target code.
        
        Args:
            prompt: The original prompt given to the model.
            response: The model's response to evaluate.
            **kwargs: Additional arguments (e.g., target_code, original_code).
            
        Returns:
            Dict containing:
                - 'reward': Float between 0.0 and 1.0
                - 'details': Dict with additional analysis information
        """
        raise NotImplementedError("Subclasses must implement verify()")

    def __call__(self, prompt: str, response: str, **kwargs) -> Dict[str, Any]:
        """
        Convenience method to call verify().
        
        Args:
            prompt: The original prompt.
            response: The model's response.
            **kwargs: Additional arguments passed to verify().
            
        Returns:
            Result from verify() method.
        """
        return self.verify(prompt, response, **kwargs)
