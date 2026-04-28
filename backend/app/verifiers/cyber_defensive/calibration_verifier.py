"""
Calibration verifier for Mythos Safe Enterprise.

This module detects over-engineering and poor calibration in model responses.
"""
import re
import logging
from typing import Dict, Any

from .base_verifier import BaseVerifier

logger = logging.getLogger(__name__)


class OverEngineeringDetector(BaseVerifier):
    """
    Verifier that detects over-engineering and poor calibration.
    
    Penalizes responses that are:
    - Excessively verbose (over 650 words)
    - Use marketing buzzwords ("highly sophisticated", "enterprise-grade")
    - Overly complex for the task at hand
    """

    def __init__(self) -> None:
        """Initialize the calibration verifier."""
        self.max_words: int = 650
        self.buzzword_pattern: str = r"(?i)highly sophisticated|enterprise-grade|multi-layered"
        logger.info("OverEngineeringDetector initialized")

    def score(self, response: str) -> float:
        """
        Calculate calibration score for a response.
        
        Args:
            response: The model's response to evaluate.
            
        Returns:
            Calibration score between 0.0 (poor) and 1.0 (well-calibrated).
        """
        score: float = 1.0
        text_lower: str = response.lower()
        
        word_count: int = len(response.split())
        if word_count > self.max_words:
            score -= 0.2
            logger.debug("Over-engineering detected: %d words (max %d)", 
                        word_count, self.max_words)
        
        if re.search(self.buzzword_pattern, text_lower):
            score -= 0.25
            logger.debug("Buzzwords detected in response")
        
        final_score = max(0.0, min(1.0, score))
        return final_score

    def verify(self, prompt: str, response: str, **kwargs) -> Dict[str, Any]:
        """
        Verify a response for calibration quality.
        
        Args:
            prompt: The original prompt (unused in this verifier).
            response: The model's response to evaluate.
            **kwargs: Additional arguments (unused).
            
        Returns:
            Dict with:
                - 'reward': Float calibration score
                - 'details': Dict with calibration_score
        """
        calib_score: float = self.score(response)
        
        return {
            "reward": round(calib_score, 4),
            "details": {"calibration_score": round(calib_score, 4)}
        }
