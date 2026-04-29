from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.db import get_db
from app.models import Incident
from app.deps import require_role

router = APIRouter()

class IncidentCreate(BaseModel):
    project_id: int
    severity: str = "medium"
    description: str

class IncidentUpdate(BaseModel):
    severity: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None  # open, investigating, resolved, closed

@router.get("/")
def list_incidents(db: Session = Depends(get_db), user=Depends(require_role("admin","engineer","auditor","viewer"))):
    return db.query(Incident).order_by(Incident.id.desc()).limit(100).all()

@router.post("/")
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db), user=Depends(require_role("admin","engineer"))):
    inc = Incident(project_id=payload.project_id, severity=payload.severity, description=payload.description)
    db.add(inc)
    db.commit()
    db.refresh(inc)
    return inc

@router.patch("/{incident_id}")
def update_incident(incident_id: int, payload: IncidentUpdate, db: Session = Depends(get_db), user=Depends(require_role("admin","engineer"))):
    inc = db.query(Incident).filter(Incident.id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    if payload.severity is not None:
        inc.severity = payload.severity
    if payload.description is not None:
        inc.description = payload.description
    if payload.status is not None:
        if payload.status not in ("open", "investigating", "resolved", "closed"):
            raise HTTPException(status_code=400, detail="Invalid status. Must be: open, investigating, resolved, closed")
        inc.status = payload.status
    db.commit()
    db.refresh(inc)
    return inc

@router.get("/report/{project_id}")
def incidents_report(project_id: int, db: Session = Depends(get_db), user=Depends(require_role("admin","auditor"))):
    incidents = db.query(Incident).filter(Incident.project_id == project_id).all()

    report = f"# Security Incidents Report - Project {project_id}\n\n"
    report += f"Total incidents: {len(incidents)}\n\n"

    for inc in incidents:
        report += f"## Incident {inc.id}\n"
        report += f"- Severity: {inc.severity}\n"
        report += f"- Status: {inc.status}\n"
        report += f"- Description: {inc.description}\n"
        report += f"- Created: {inc.created_at}\n\n"

    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(report, media_type="text/markdown")
