from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db
from app.models import Dataset
from app.deps import require_role

router = APIRouter()

class DatasetCreate(BaseModel):
    project_id: int
    name: str
    description: str = ""
    uri: str = ""

@router.get("/")
def list_datasets(db: Session = Depends(get_db), user=Depends(require_role("admin","engineer","auditor","viewer"))):
    return db.query(Dataset).all()

@router.post("/")
def create_dataset(payload: DatasetCreate, db: Session = Depends(get_db), user=Depends(require_role("admin","engineer"))):
    d = Dataset(**payload.model_dump())
    db.add(d)
    db.commit()
    db.refresh(d)
    return d
