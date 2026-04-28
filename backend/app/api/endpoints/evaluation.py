"""
API endpoints for cyber defensive evaluation.

This module provides the FastAPI routes for running cyber defensive
evaluations and retrieving results.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.verification import CyberEvaluationRequest, CyberEvaluationResponse
from app.services.verification_service import VerificationService
from app.models.evaluation import CyberEvaluationResult
from uuid import uuid4
import hashlib
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/evaluation", tags=["evaluation"])
verification_service = VerificationService()


@router.post("/cyber-defensive", response_model=CyberEvaluationResponse)
async def evaluate_cyber_defensive(
    request: CyberEvaluationRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Run defensive cyber evaluation using Mythos++ verifiers.
    
    This endpoint evaluates model responses for:
    - Vulnerability detection accuracy
    - Safe patching practices
    - Anti-hacking compliance
    - Calibration quality
    
    Args:
        request: CyberEvaluationRequest containing prompt, response, and target_code.
        db: Database session (injected).
        current_user: Authenticated user (injected).
        
    Returns:
        Dict containing:
            - status: 'completed' or 'rejected'
            - composite_reward: Weighted score (0.0 to 1.0)
            - vuln_analysis: Vulnerability scan results
            - patch_analysis: Patch verification results
            - safety: Anti-hacking results
            - calibration: Calibration results
            - evaluation_id: Unique identifier for this evaluation
            
    Raises:
        HTTPException: If evaluation fails or user is unauthorized.
    """
    try:
        eval_id: str = request.evaluation_id or str(uuid4())
        payload: Dict[str, Any] = request.dict()

        logger.info(
            "Starting cyber evaluation %s for user %s",
            eval_id, current_user.id
        )

        result: Dict[str, Any] = await verification_service.run_cyber_defensive_evaluation(
            payload
        )

        # Save result to database
        try:
            db_result = CyberEvaluationResult(
                evaluation_id=eval_id,
                user_id=current_user.id,
                prompt=request.prompt,
                target_code_hash=hashlib.sha256(
                    request.target_code.encode()
                ).hexdigest(),
                composite_reward=result.get("composite_reward", 0.0),
                vuln_analysis=result.get("vuln_analysis"),
                patch_analysis=result.get("patch_analysis"),
                safety_analysis=result.get("safety"),
                calibration_analysis=result.get("calibration"),
                status=result.get("status", "error")
            )
            db.add(db_result)
            db.commit()
            db.refresh(db_result)
            logger.info("Saved evaluation %s to database", eval_id)
        except Exception as db_error:
            logger.error("Failed to save evaluation to DB: %s", db_error)
            db.rollback()
            # Continue without DB save - don't fail the evaluation

        return {**result, "evaluation_id": eval_id}

    except ValueError as e:
        logger.error("Invalid request: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.exception("Evaluation failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Evaluation failed: {str(e)}"
        )


@router.get("/cyber-defensive/{evaluation_id}")
async def get_evaluation_result(
    evaluation_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Retrieve a previous evaluation result by ID.
    
    Args:
        evaluation_id: The unique evaluation identifier.
        db: Database session (injected).
        current_user: Authenticated user (injected).
        
    Returns:
        The evaluation result if found and authorized.
        
    Raises:
        HTTPException: If evaluation not found or unauthorized.
    """
    try:
        result = db.query(CyberEvaluationResult).filter(
            CyberEvaluationResult.evaluation_id == evaluation_id,
            CyberEvaluationResult.user_id == current_user.id
        ).first()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evaluation not found"
            )

        return {
            "evaluation_id": result.evaluation_id,
            "status": result.status,
            "composite_reward": result.composite_reward,
            "vuln_analysis": result.vuln_analysis,
            "patch_analysis": result.patch_analysis,
            "safety": result.safety_analysis,
            "calibration": result.calibration_analysis,
            "created_at": result.created_at
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Failed to retrieve evaluation: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve evaluation"
        )
