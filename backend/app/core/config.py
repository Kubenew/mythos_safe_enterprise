"""
Configuration settings for Mythos Safe Enterprise.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Core
    PROJECT_NAME: str = "Mythos Safe Enterprise"
    API_V1_STR: str = "/api"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./mythos.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
