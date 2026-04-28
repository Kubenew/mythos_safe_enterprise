from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db
from app.models import Project
from app.deps import require_role

router = APIRouter()

class ProjectCreate(BaseModel):
    name: str
    description: str = ""

@router.get("/")
def list_projects(db: Session = Depends(get_db), user=Depends(require_role("admin","engineer","auditor","viewer"))):
    return db.query(Project).all()

@router.post("/")
def create_project(payload: ProjectCreate, db: Session = Depends(get_db), user=Depends(require_role("admin","engineer"))):
    p = Project(name=payload.name, description=payload.description)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p
