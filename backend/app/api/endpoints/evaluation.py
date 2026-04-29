# backend/app/api/endpoints/evaluation.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import hashlib
from uuid import uuid4

from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.verification import CyberEvaluationRequest, CyberEvaluationResponse
from app.services.verification_service import VerificationService
from app.models.evaluation import CyberEvaluationResult
from app.worker.tasks import run_cyber_defensive_task

router = APIRouter(prefix="/evaluation", tags=["evaluation"])

verification_service = VerificationService()


@router.post("/cyber-defensive", response_model=CyberEvaluationResponse)
async def evaluate_cyber_defensive(
    request: CyberEvaluationRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    use_celery: bool = False
):
    """Defensive cyber evaluation endpoint - supports sync and async modes."""
    eval_id = request.evaluation_id or str(uuid4())

    if use_celery:
        # Async via Celery
        task = run_cyber_defensive_task.delay(
            payload=request.dict(),
            user_id=current_user.id
        )
        return {
            "status": "queued",
            "evaluation_id": eval_id,
            "task_id": task.id,
            "message": "Evaluation queued for background processing"
        }

    # Synchronous evaluation
    try:
        result = await verification_service.run_cyber_defensive_evaluation(request.dict())

        # Persist result
        db_result = CyberEvaluationResult(
            evaluation_id=eval_id,
            user_id=current_user.id,
            prompt=request.prompt,
            target_code_hash=hashlib.sha256(request.target_code.encode()).hexdigest(),
            composite_reward=result["composite_reward"],
            vuln_analysis=result.get("vuln_analysis"),
            patch_analysis=result.get("patch_analysis"),
            safety_analysis=result.get("safety"),
            calibration_analysis=result.get("calibration"),
            status=result["status"]
        )
        db.add(db_result)
        db.commit()
        db.refresh(db_result)

        return {**result, "evaluation_id": eval_id}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Evaluation failed: {str(e)}"
        )
