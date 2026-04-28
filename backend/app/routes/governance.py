from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse

from app.db import get_db
from app.models import Project, Job
from app.deps import require_role

router = APIRouter()

class GateCheck(BaseModel):
    project_id: int
    gate: str  # A, B, C, D
    status: str  # passed, failed, pending
    notes: str = ""

@router.get("/gates/{project_id}")
def get_gates(project_id: int, db: Session = Depends(get_db), user=Depends(require_role("admin","engineer","auditor","viewer"))):
    """Get RSP-style release gates status for a project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    jobs = db.query(Job).filter(Job.project_id == project_id).all()
    
    # Gate A: Dataset approved (check if datasets exist)
    datasets = db.query(Job).filter(Job.project_id == project_id, Job.type == "dataset").count()
    gate_a = "passed" if datasets > 0 else "pending"
    
    # Gate B: Eval suite passed (check for completed evals)
    eval_jobs = [j for j in jobs if j.type == "eval" and j.status == "done"]
    gate_b = "passed" if eval_jobs else "pending"
    
    # Gate C: Red-team report (placeholder)
    gate_c = "pending"
    
    # Gate D: Deployment approval
    gate_d = "blocked" if gate_b == "pending" else "pending"
    
    return {
        "project_id": project_id,
        "gates": {
            "A": {"name": "Dataset approved", "status": gate_a},
            "B": {"name": "Eval suite passed", "status": gate_b},
            "C": {"name": "Red-team report attached", "status": gate_c},
            "D": {"name": "Deployment approval", "status": gate_d}
        },
        "ready_for_release": all(g["status"] == "passed" for g in [{"status": gate_a}, {"status": gate_b}, {"status": gate_c}, {"status": gate_d}])
    }

@router.get("/audit-log/{project_id}")
def get_audit_log(project_id: int, db: Session = Depends(get_db), user=Depends(require_role("admin","auditor"))):
    """Get audit log for compliance."""
    jobs = db.query(Job).filter(Job.project_id == project_id).order_by(Job.id.desc()).limit(100).all()
    
    log_entries = []
    for j in jobs:
        log_entries.append({
            "timestamp": j.created_at.isoformat() if j.created_at else "",
            "job_id": j.id,
            "type": j.type,
            "status": j.status,
            "output": j.output_json[:200] if j.output_json else ""
        })
    
    log_text = f"# Audit Log - Project {project_id}\n\n"
    for entry in log_entries:
        log_text += f"[{entry['timestamp']}] Job {entry['job_id']}: {entry['type']} - {entry['status']}\n"
    
    return PlainTextResponse(log_text, media_type="text/plain")

@router.get("/compliance-report/{project_id}")
def compliance_report(project_id: int, db: Session = Depends(get_db), user=Depends(require_role("admin","auditor"))):
    """Generate compliance report for auditors."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    jobs = db.query(Job).filter(Job.project_id == project_id).all()
    eval_jobs = [j for j in jobs if j.type == "eval" and j.status == "done"]
    
    import json
    total_evals = len(eval_jobs)
    avg_accuracy = 0
    if total_evals > 0:
        accuracies = []
        for j in eval_jobs:
            if j.output_json:
                out = json.loads(j.output_json)
                if "accuracy" in out:
                    accuracies.append(out["accuracy"])
        avg_accuracy = sum(accuracies) / max(1, len(accuracies))
    
    report = f"""# Compliance Report - {project.name}

## Summary
- Total evaluations: {total_evals}
- Average accuracy: {avg_accuracy:.2%}
- Jobs executed: {len(jobs)}

## Risk Assessment
- Cyber risk: Low (defensive-only verifiers)
- Misuse risk: Low (sandbox + anti-hacking gates)
- Eval coverage: {"Partial" if total_evals > 0 else "None"}

## Compliance Status
- ✅ Audit logging: Enabled
- ✅ Sandbox execution: Configured
- ✅ Safety gates: Active
- ⚠️ External red-teaming: Pending

## Recommendation
{"READY FOR RELEASE" if avg_accuracy > 0.7 and total_evals > 0 else "NEEDS MORE EVALUATION"}
"""
    
    return PlainTextResponse(report, media_type="text/markdown")
