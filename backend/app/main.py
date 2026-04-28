from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import init_db
from app.routes import auth, projects, models, datasets, jobs, reports, governance, incidents
from app.api.endpoints import evaluation

app = FastAPI(title="Mythos-Safe Enterprise API", version="1.0.0")

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
def root():
    return {"status": "ok"}
