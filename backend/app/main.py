"""Mythos-Safe Enterprise API (MVP).

This repo originally contained two competing backend layouts:
- app.routes.* (simple MVP style)
- app.api.endpoints.* expecting app.core.* modules

The app.core.* modules do not exist in this repository.
This main.py is patched to use the existing working MVP routes.

If you later want a cleaner architecture, migrate everything into
app/api/endpoints/ and create app/core/*.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import init_db
from app.routes import auth, projects, models, datasets, jobs, reports, governance, incidents

app = FastAPI(
    title="Mythos Safe Enterprise",
    description="Enterprise platform for safe LLM evaluation and governance (defensive-only)",
    version="1.0.0",
)

# CORS (MVP default permissive)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


# API Routers
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(projects.router, prefix="/api/v1", tags=["projects"])
app.include_router(models.router, prefix="/api/v1", tags=["models"])
app.include_router(datasets.router, prefix="/api/v1", tags=["datasets"])
app.include_router(jobs.router, prefix="/api/v1", tags=["jobs"])
app.include_router(reports.router, prefix="/api/v1", tags=["reports"])
app.include_router(governance.router, prefix="/api/v1", tags=["governance"])
app.include_router(incidents.router, prefix="/api/v1", tags=["incidents"])


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}


@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Mythos Safe Enterprise API",
        "version": "1.0.0",
        "docs": "/docs",
        "api": "/api/v1",
    }
