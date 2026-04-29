import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db
from app.models import Job
from app.deps import require_role
from app.celery_app import celery

router = APIRouter()

class JobCreate(BaseModel):
    project_id: int
    type: str
    input: dict = {}

@router.get("/")
def list_jobs(db: Session = Depends(get_db), user=Depends(require_role("admin","engineer","auditor","viewer"))):
    return db.query(Job).order_by(Job.id.desc()).limit(200).all()

@router.post("/")
def create_job(payload: JobCreate, db: Session = Depends(get_db), user=Depends(require_role("admin","engineer"))):
    job = Job(project_id=payload.project_id, type=payload.type, status="queued", input_json=json.dumps(payload.input))
    db.add(job)
    db.commit()
    db.refresh(job)
    celery.send_task("worker.tasks.run_job", args=[job.id])
    return job
