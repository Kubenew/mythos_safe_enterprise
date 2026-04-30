# backend/app/models/evaluation.py
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.core.database import Base

class CyberEvaluationResult(Base):
    __tablename__ = "cyber_evaluation_results"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(String(36), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    prompt = Column(Text, nullable=False)
    target_code_hash = Column(String(64), nullable=False)

    composite_reward = Column(Float, nullable=False)
    vuln_analysis = Column(JSON, nullable=True)
    patch_analysis = Column(JSON, nullable=True)
    safety_analysis = Column(JSON, nullable=True)
    calibration_analysis = Column(JSON, nullable=True)

    status = Column(String(20), default="completed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<CyberEvaluationResult {self.evaluation_id} reward={self.composite_reward}>"
