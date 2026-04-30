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


@shared_task(name="cyber_defensive_evaluation", bind=True, max_retries=3, queue="cyber_evaluation")
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
            composite_reward=result.get("composite_reward", 0.0),
            vuln_analysis=result.get("vuln_analysis"),
            patch_analysis=result.get("patch_analysis"),
            safety_analysis=result.get("safety"),
            calibration_analysis=result.get("calibration"),
            status=result.get("status", "completed")
        )

        db.add(db_result)
        db.commit()

        logger.info(f"✅ Cyber evaluation completed: {eval_id} | Reward: {result.get('composite_reward', 0):.4f}")
        return {"task_id": self.request.id, "evaluation_id": eval_id, "status": result.get("status")}

    except Exception as exc:
        logger.error(f"❌ Task failed for {eval_id}: {exc}")
        db.rollback()
        raise self.retry(countdown=60, exc=exc)
    finally:
        db.close()