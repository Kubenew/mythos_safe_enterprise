"""
Main application module for Mythos Safe Enterprise.

This module initializes the FastAPI application with security middleware,
CORS configuration, and all API routers.
"""
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import logging

from app.db import init_db
from app.routes import auth, projects, models, datasets, jobs, reports, governance, incidents
from app.api.endpoints import evaluation

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses.
    
    Adds headers like X-Content-Type-Options, X-Frame-Options,
    and Strict-Transport-Security to enhance security.
    """
    
    async def dispatch(self, request: Request, call_next):
        """Add security headers to response."""
        response: Response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response


app = FastAPI(
    title="Mythos-Safe Enterprise API",
    version="1.0.0",
    description="Enterprise-grade platform for safe LLM evaluation and governance"
)

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# CORS configuration (should be restricted in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production!
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    """Initialize database on startup."""
    logger.info("Starting Mythos Safe Enterprise API")
    init_db()
    logger.info("Database initialized")


@app.on_event("shutdown")
def shutdown():
    """Cleanup on shutdown."""
    logger.info("Shutting down Mythos Safe Enterprise API")


# Include all routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(models.router, prefix="/models", tags=["models"])
app.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(governance.router, prefix="/governance", tags=["governance"])
app.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
app.include_router(evaluation.router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "version": "1.0.0"}


@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "service": "mythos-safe-enterprise",
        "version": "1.0.0"
    }
