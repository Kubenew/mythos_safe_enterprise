from typing import Dict, Any
from .base_verifier import BaseVerifier

class MathVerifier(BaseVerifier):
    """Math exact-match verifier for RLVR."""

    def verify(self, prompt: str, response: str, **kwargs) -> Dict[str, Any]:
        expected = kwargs.get("expected", "")
        got = response.strip()
        
        reward = 1.0 if expected.strip() == got else 0.0
        
        return {
            "reward": reward,
            "details": {"match": expected.strip() == got, "expected": expected, "got": got}
        }
