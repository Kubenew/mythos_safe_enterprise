import re
from typing import Dict, Any

class OverEngineeringDetector:
    """Detects over-engineering and calibration issues."""
    
    def score(self, response: str) -> float:
        """Returns calibration score [0.0 bad -> 1.0 good]"""
        text = response.lower()
        
        # Good: concise, focused answers
        good_signals = sum(0.15 for kw in ["precisely", "specifically", "the vulnerability", "this code"] if kw in text)
        
        # Bad: over-engineered, verbose, vague
        bad_signals = sum(0.1 for kw in ["additionally", "furthermore", "moreover", "comprehensive", "extensive"] if kw in text)
        
        # Penalize excessive length without substance
        words = text.split()
        if len(words) > 500:
            bad_signals += 0.3
        
        return max(0.0, min(1.0, 0.5 + good_signals - bad_signals))
    
    def verify(self, prompt: str, response: str, **kwargs) -> Dict[str, Any]:
        score = self.score(response)
        return {
            "reward": round(score, 4),
            "details": {"calibration_score": round(score, 4), "status": "accepted"}
        }
