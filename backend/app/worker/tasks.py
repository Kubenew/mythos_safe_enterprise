# backend/app/worker/tasks.py
from celery import shared_task
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.verification_service import VerificationService
from app.models.evaluation import CyberEvaluationResult
import hashlib
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)
verification_service = VerificationService()


@shared_task(name="cyber_defensive_evaluation", bind=True, max_retries=3)
def run_cyber_defensive_task(self, payload: dict, user_id: int):
    db: Session = SessionLocal()
    eval_id = payload.get("evaluation_id") or str(uuid4())

    try:
        result = verification_service.run_cyber_defensive_evaluation(payload)

        db_result = CyberEvaluationResult(
            evaluation_id=eval_id,
            user_id=user_id,
            prompt=payload["prompt"],
            target_code_hash=hashlib.sha256(payload["target_code"].encode()).hexdigest(),
            composite_reward=result["composite_reward"],
            vuln_analysis=result.get("vuln_analysis"),
            patch_analysis=result.get("patch_analysis"),
            safety_analysis=result.get("safety"),
            calibration_analysis=result.get("calibration"),
            status=result["status"]
        )

        db.add(db_result)
        db.commit()

        logger.info(f"Cyber evaluation completed: {eval_id} | Reward: {result['composite_reward']:.4f}")
        return {"evaluation_id": eval_id, "status": result["status"]}

    except Exception as exc:
        logger.error(f"Task failed: {exc}")
        db.rollback()
        raise self.retry(countdown=60, exc=exc)
    finally:
        db.close()
