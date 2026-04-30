# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db

# Import routers from routes/ (not api.endpoints)
from app.routes import auth, projects, models, datasets, jobs, reports, governance, incidents
from app.routes import evaluation

app = FastAPI(
    title=settings.PROJECT_NAME,
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

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(models.router, prefix="/models", tags=["models"])
app.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(governance.router, prefix="/governance", tags=["governance"])
app.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
app.include_router(evaluation.router, prefix=settings.API_V1_STR, tags=["evaluation"])


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "service": "mythos-safe-enterprise"}


@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Mythos Safe Enterprise API",
        "version": "1.0.0",
        "docs": "/docs"
    }
