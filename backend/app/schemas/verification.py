# backend/app/schemas/verification.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class CyberEvaluationRequest(BaseModel):
    """Request for defensive cyber evaluation."""
    prompt: str = Field(..., min_length=10, description="Prompt given to the model")
    response: str = Field(..., min_length=20, description="Model's full response")
    target_code: str = Field(..., description="Code being analyzed")
    original_code: Optional[str] = Field(None, description="Original code before proposed patch")
    evaluation_id: Optional[str] = Field(None, description="Custom evaluation ID")

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Analyze this code for security vulnerabilities.",
                "response": "Detected SQL injection risk...",
                "target_code": "SELECT * FROM users WHERE id = " + user_input
            }
        }


class CyberEvaluationResponse(BaseModel):
    """Response from cyber defensive evaluation."""
    status: str
    composite_reward: float
    evaluation_id: Optional[str] = None
    vuln_analysis: Dict[str, Any]
    patch_analysis: Dict[str, Any]
    safety: Dict[str, Any]
    calibration: Dict[str, Any]
    message: Optional[str] = None
    created_at: Optional[datetime] = None
