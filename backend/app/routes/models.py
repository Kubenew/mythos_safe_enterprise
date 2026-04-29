from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db
from app.models import ModelRegistry
from app.deps import require_role

router = APIRouter()

class ModelCreate(BaseModel):
    project_id: int
    name: str
    version: str
    endpoint: str = ""

@router.get("/")
def list_models(db: Session = Depends(get_db), user=Depends(require_role("admin","engineer","auditor","viewer"))):
    return db.query(ModelRegistry).all()

@router.post("/")
def create_model(payload: ModelCreate, db: Session = Depends(get_db), user=Depends(require_role("admin","engineer"))):
    m = ModelRegistry(**payload.model_dump())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m
