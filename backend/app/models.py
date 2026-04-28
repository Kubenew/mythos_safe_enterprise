from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="viewer", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ModelRegistry(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(200), nullable=False)
    version = Column(String(50), nullable=False)
    endpoint = Column(String(500), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    project = relationship("Project")

class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, default="")
    uri = Column(String(500), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    project = relationship("Project")

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    type = Column(String(50), nullable=False)
    status = Column(String(50), default="queued")
    input_json = Column(Text, default="{}")
    output_json = Column(Text, default="{}")
    logs = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    project = relationship("Project")
