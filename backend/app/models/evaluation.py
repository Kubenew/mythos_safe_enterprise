from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db import Base # Changed from app.core.database

class CyberEvaluationResult(Base):
    __tablename__ = "cyber_evaluation_results"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(String(36), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    prompt = Column(Text, nullable=False)
    target_code_hash = Column(String(64), nullable=False)

    composite_reward = Column(Float, nullable=False)
    vuln_analysis = Column(JSON)
    patch_analysis = Column(JSON)
    safety_analysis = Column(JSON)
    calibration_analysis = Column(JSON)

    status = Column(String(20), default="completed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
