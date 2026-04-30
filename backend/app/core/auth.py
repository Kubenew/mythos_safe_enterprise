"""
Authentication utilities for Mythos Safe Enterprise.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import BaseModel

from app.core.config import settings
from app.db import SessionLocal


class TokenData(BaseModel):
    """JWT token payload."""
    email: str
    role: str


http_bearer = HTTPBearer()


def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(http_bearer),
    db: Session = Depends(get_db)
):
    """Get current authenticated user from JWT token."""
    try:
        payload = jwt.decode(
            token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        role: str = payload.get("role", "viewer")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return TokenData(email=email, role=role)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


def require_role(*allowed_roles: str):
    """Dependency to require specific user roles."""
    def role_checker(user=Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return role_checker
