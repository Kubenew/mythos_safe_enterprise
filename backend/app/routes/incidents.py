from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.db import get_db, Base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, func
from app.deps import require_role

router = APIRouter()

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=False)
    severity = Column(String(50), default="medium")
    description = Column(Text, default="")
    status = Column(String(50), default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Create table
try:
    Base.metadata.create_all(bind=Base.metadata.bind)
except:
    pass

class IncidentCreate(BaseModel):
    project_id: int
    severity: str = "medium"
    description: str

@router.get("/")
def list_incidents(db: Session = Depends(get_db), user=Depends(require_role("admin","engineer","auditor","viewer"))):
    try:
        incidents = db.query(Incident).order_by(Incident.id.desc()).limit(100).all()
        return incidents
    except:
        return []

@router.post("/")
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db), user=Depends(require_role("admin","engineer"))):
    try:
        inc = Incident(project_id=payload.project_id, severity=payload.severity, description=payload.description)
        db.add(inc)
        db.commit()
        db.refresh(inc)
        return inc
    except Exception as e:
        return {"error": "Incidents table not ready. Run init_db first."}

@router.get("/report/{project_id}")
def incidents_report(project_id: int, db: Session = Depends(get_db), user=Depends(require_role("admin","auditor"))):
    try:
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
    except:
        return {"error": "Incidents feature not available yet"}
