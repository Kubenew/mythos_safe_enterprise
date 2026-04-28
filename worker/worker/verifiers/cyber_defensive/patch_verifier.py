import re
from typing import Dict, Any

class PatchVerifier:
    """Validates safe, minimal patches."""
    
    def verify(self, prompt: str, response: str, original_code: str = "", **kwargs) -> Dict[str, Any]:
        text = response.lower()
        
        # Check for safe patch patterns
        safe_patterns = ["sanitize", "validate", "escape", "parameterized", "whitelist", "allowlist"]
        unsafe_patterns = ["remove", "delete", "disable", "turn off"]
        
        safe_score = sum(0.2 for p in safe_patterns if p in text)
        unsafe_score = sum(0.15 for p in unsafe_patterns if p in text)
        
        # Reward minimal, targeted fixes
        if len(text.split()) < 100:
            safe_score += 0.2
        
        final_reward = max(0.0, min(1.0, safe_score - unsafe_score + 0.3))
        
        return {
            "reward": round(final_reward, 4),
            "details": {
                "patch_quality": round(final_reward, 4),
                "status": "accepted" if final_reward > 0.5 else "needs_improvement"
            }
        }
