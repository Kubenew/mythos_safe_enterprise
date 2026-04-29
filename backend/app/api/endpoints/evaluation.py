from fastapi import APIRouter, Depends
from app.schemas.verification import CyberEvaluationRequest, CyberEvaluationResponse
from app.services.verification_service import VerificationService
from app.deps import require_role

router = APIRouter(prefix="/evaluation", tags=["evaluation"])
service = VerificationService()


@router.post("/cyber-defensive", response_model=CyberEvaluationResponse)
async def evaluate_cyber_defensive(
    request: CyberEvaluationRequest,
    user=Depends(require_role("admin", "engineer"))
):
    result = await service.run_cyber_defensive_evaluation(request.dict())
    return result
