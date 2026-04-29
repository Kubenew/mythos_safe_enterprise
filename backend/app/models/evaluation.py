from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db import Base


class CyberEvaluationResult(Base):
    __tablename__ = "cyber_evaluation_results"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    prompt = Column(String, nullable=False)
    target_code_hash = Column(String, nullable=False)  # SHA256 hash for privacy
    composite_reward = Column(Float, nullable=False)
    
    vuln_analysis = Column(JSON)
    patch_analysis = Column(JSON)
    safety_analysis = Column(JSON)
    calibration_analysis = Column(JSON)
    
    status = Column(String, default="completed")  # completed, rejected, error
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<CyberEvaluationResult {self.evaluation_id} reward={self.composite_reward}>"
