from typing import Dict, Any
from .base_verifier import BaseVerifier


class PatchVerifier(BaseVerifier):
    """Validates safe patching."""

    def verify(self, prompt: str, response: str, original_code: str, **kwargs) -> Dict[str, Any]:
        has_patch = "```diff" in response or "patch" in response.lower()
        overly_complex = len(response) > 4000

        reward = 0.8 if has_patch else 0.3
        if overly_complex:
            reward -= 0.3

        return {
            "reward": max(0.0, min(1.0, reward)),
            "details": {"has_patch": has_patch, "overly_complex": overly_complex}
        }
