from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class CyberEvaluationRequest(BaseModel):
    prompt: str = Field(..., description="The task prompt given to the model")
    response: str = Field(..., description="Model's full response")
    target_code: str = Field(..., description="Code being analyzed for vulnerabilities")
    original_code: Optional[str] = Field(None, description="Original code before proposed patch")
    evaluation_id: Optional[str] = None


class CyberEvaluationResponse(BaseModel):
    status: str
    composite_reward: float
    vuln_analysis: Dict[str, Any]
    patch_analysis: Dict[str, Any]
    safety: Dict[str, Any]
    calibration: Dict[str, Any]
    scan_result: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
