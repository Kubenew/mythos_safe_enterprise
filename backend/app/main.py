# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.endpoints import auth, users, evaluation

app = FastAPI(
    title="Mythos Safe Enterprise",
    description="Enterprise platform for safe LLM evaluation and defensive cybersecurity (Mythos++)",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])
app.include_router(evaluation.router, prefix=settings.API_V1_STR, tags=["evaluation"])

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}

@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Mythos Safe Enterprise API",
        "version": "1.0.0",
        "docs": "/docs"
    }