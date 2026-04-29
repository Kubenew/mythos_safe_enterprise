import re
from typing import Dict, Any
from .base_verifier import BaseVerifier

class OverEngineeringDetector(BaseVerifier):
    def score(self, response: str) -> float:
        score = 1.0
        text = response.lower()
        if len(response.split()) > 650:
            score -= 0.2
        if re.search(r"(?i)highly sophisticated|enterprise-grade|multi-layered", text):
            score -= 0.25
        return max(0.0, min(1.0, score))

    def verify(self, prompt: str, response: str, **kwargs) -> Dict[str, Any]:
        calib_score = self.score(response)
        return {
            "reward": round(calib_score, 4),
            "details": {"calibration_score": round(calib_score, 4)}
        }
