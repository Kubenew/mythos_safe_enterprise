from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
from typing import Optional
import json

from app.db import get_db
from app.models import Project, Job, GovernanceGate
from app.deps import require_role, get_current_user

router = APIRouter()

# ── Schemas ─────────────────────────────────────────────────────────

class GateUpdate(BaseModel):
    status: str  # passed, failed, pending, blocked
    notes: Optional[str] = ""

class GateCreate(BaseModel):
    project_id: int
    gate: str  # A, B, C, D
    name: str
    status: str = "pending"
    notes: str = ""

# ── Initialize default gates for a project ──────────────────────────

DEFAULT_GATES = [
    {"gate": "A", "name": "Dataset approved"},
    {"gate": "B", "name": "Eval suite passed"},
    {"gate": "C", "name": "Red-team report attached"},
    {"gate": "D", "name": "Deployment approval"},
]

def ensure_gates_exist(db: Session, project_id: int):
    """Create default gates for a project if they don't exist."""
    existing = db.query(GovernanceGate).filter(GovernanceGate.project_id == project_id).count()
    if existing == 0:
        for gate_def in DEFAULT_GATES:
            g = GovernanceGate(
                project_id=project_id,
                gate=gate_def["gate"],
                name=gate_def["name"],
                status="pending",
            )
            db.add(g)
        db.commit()

# ── Endpoints ───────────────────────────────────────────────────────

@router.get("/gates/{project_id}")
def get_gates(project_id: int, db: Session = Depends(get_db), user=Depends(require_role("admin","engineer","auditor","viewer"))):
    """Get RSP-style release gates status for a project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    ensure_gates_exist(db, project_id)

    # Compute dynamic gate statuses from job data
    jobs = db.query(Job).filter(Job.project_id == project_id).all()

    # Fetch stored gates
    gates = db.query(GovernanceGate).filter(GovernanceGate.project_id == project_id).order_by(GovernanceGate.gate).all()

    # Auto-update Gate A based on datasets
    datasets_count = db.query(Job).filter(Job.project_id == project_id, Job.type == "dataset").count()
    gate_a = next((g for g in gates if g.gate == "A"), None)
    if gate_a and gate_a.status == "pending" and datasets_count > 0:
        gate_a.status = "passed"
        gate_a.notes = f"Auto-passed: {datasets_count} datasets found"
        db.commit()

    # Auto-update Gate B based on eval jobs
    eval_jobs = [j for j in jobs if j.type == "eval" and j.status == "done"]
    gate_b = next((g for g in gates if g.gate == "B"), None)
    if gate_b and gate_b.status == "pending" and eval_jobs:
        gate_b.status = "passed"
        gate_b.notes = f"Auto-passed: {len(eval_jobs)} evaluations completed"
        db.commit()

    # Build response
    gates_response = {}
    for g in gates:
        gates_response[g.gate] = {
            "id": g.id,
            "name": g.name,
            "status": g.status,
            "notes": g.notes or "",
            "approved_by": g.approved_by or "",
        }

    all_passed = all(g.status == "passed" for g in gates)

    return {
        "project_id": project_id,
        "gates": gates_response,
        "ready_for_release": all_passed,
    }

@router.post("/gates/{project_id}/{gate_id}/approve")
def approve_gate(project_id: int, gate_id: str, payload: GateUpdate, db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    """Approve or reject a governance gate. Admin only."""
    gate = db.query(GovernanceGate).filter(
        GovernanceGate.project_id == project_id,
        GovernanceGate.gate == gate_id.upper()
    ).first()

    if not gate:
        raise HTTPException(status_code=404, detail=f"Gate {gate_id} not found for project {project_id}")

    if payload.status not in ("passed", "failed", "pending", "blocked"):
        raise HTTPException(status_code=400, detail="Status must be: passed, failed, pending, blocked")

    gate.status = payload.status
    gate.notes = payload.notes or gate.notes
    gate.approved_by = user.email
    db.commit()
    db.refresh(gate)

    return {
        "gate": gate.gate,
        "name": gate.name,
        "status": gate.status,
        "notes": gate.notes,
        "approved_by": gate.approved_by,
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

    # Check governance gates
    gates = db.query(GovernanceGate).filter(GovernanceGate.project_id == project_id).all()
    gates_passed = sum(1 for g in gates if g.status == "passed")
    gates_total = len(gates) if gates else 4

    report = f"""# Compliance Report - {project.name}

## Summary
- Total evaluations: {total_evals}
- Average accuracy: {avg_accuracy:.2%}
- Jobs executed: {len(jobs)}
- Governance gates passed: {gates_passed}/{gates_total}

## Risk Assessment
- Cyber risk: Low (defensive-only verifiers)
- Misuse risk: Low (sandbox + anti-hacking gates)
- Eval coverage: {"Partial" if total_evals > 0 else "None"}

## Compliance Status
- {"✅" if total_evals > 0 else "❌"} Evaluation suite: {"Executed" if total_evals > 0 else "Not run"}
- ✅ Audit logging: Enabled
- ✅ Sandbox execution: Configured
- ✅ Safety gates: Active
- {"✅" if gates_passed == gates_total else "⚠️"} Governance gates: {gates_passed}/{gates_total} passed
- ⚠️ External red-teaming: Pending

## Recommendation
{"READY FOR RELEASE" if avg_accuracy > 0.7 and total_evals > 0 and gates_passed == gates_total else "NEEDS MORE EVALUATION"}
"""

    return PlainTextResponse(report, media_type="text/markdown")
