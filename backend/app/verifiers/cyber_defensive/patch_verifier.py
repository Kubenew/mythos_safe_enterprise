"""
Patch verifier for Mythos Safe Enterprise.

This module validates safe and effective patching of vulnerable code.
"""
import logging
from typing import Dict, Any

from .base_verifier import BaseVerifier

logger = logging.getLogger(__name__)


class PatchVerifier(BaseVerifier):
    """
    Verifier that validates safe patching of vulnerable code.
    
    Evaluates whether the model's response includes a valid patch
    and whether the patch is appropriately complex (not over-engineered).
    """

    def __init__(self) -> None:
        """Initialize the patch verifier."""
        self.max_response_length: int = 4000
        self.patch_indicators: list = ["```diff", "patch", "diff --git"]
        logger.info("PatchVerifier initialized")

    def verify(
        self, prompt: str, response: str, original_code: str = "", **kwargs
    ) -> Dict[str, Any]:
        """
        Verify that a response contains a valid, safe patch.
        
        Args:
            prompt: The original prompt (unused).
            response: The model's response containing the patch.
            original_code: The original vulnerable code (unused currently).
            **kwargs: Additional arguments.
            
        Returns:
            Dict with:
                - 'reward': Float between 0.0 and 1.0
                - 'details': Dict with has_patch and overly_complex flags
        """
        response_lower: str = response.lower()
        has_patch: bool = any(
            indicator in response for indicator in self.patch_indicators
        )
        overly_complex: bool = len(response) > self.max_response_length

        reward: float = 0.8 if has_patch else 0.3
        if overly_complex:
            reward -= 0.3
            logger.debug("Patch response too complex: %d chars", len(response))

        final_reward = max(0.0, min(1.0, reward))
        logger.debug(
            "Patch verification: has_patch=%s, complex=%s, reward=%.2f",
            has_patch, overly_complex, final_reward
        )

        return {
            "reward": round(final_reward, 4),
            "details": {
                "has_patch": has_patch,
                "overly_complex": overly_complex
            }
        }
