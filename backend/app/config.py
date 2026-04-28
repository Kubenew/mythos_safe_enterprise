from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str = "mythos"
    POSTGRES_PASSWORD: str = "mythos"
    POSTGRES_DB: str = "mythos"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    REDIS_URL: str = "redis://redis:6379/0"

    JWT_SECRET: str = "CHANGE_ME"
    JWT_EXPIRE_MINUTES: int = 1440

    class Config:
        env_file = ".env"

settings = Settings()
