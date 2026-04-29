from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class CyberEvaluationRequest(BaseModel):
    prompt: str
    response: str
    target_code: str
    original_code: Optional[str] = None
    evaluation_id: Optional[str] = None


class CyberEvaluationResponse(BaseModel):
    status: str
    composite_reward: float
    evaluation_id: Optional[str] = None
    vuln_analysis: Dict[str, Any]
    patch_analysis: Dict[str, Any]
    safety: Dict[str, Any]
    calibration: Dict[str, Any]
    message: Optional[str] = None
