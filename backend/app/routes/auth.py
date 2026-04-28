from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db
from app.models import User
from app.security import verify_password, create_token, hash_password

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_token(user.email, user.role), "token_type": "bearer", "role": user.role}

@router.post("/seed-admin")
def seed_admin(db: Session = Depends(get_db)):
    admin = db.query(User).filter(User.email == "admin@local").first()
    if admin:
        return {"status": "exists"}
    u = User(email="admin@local", password_hash=hash_password("admin123"), role="admin")
    db.add(u)
    db.commit()
    return {"status": "created"}
