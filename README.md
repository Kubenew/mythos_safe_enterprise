# Mythos-Safe Enterprise MVP

Enterprise-grade AI platform for safe LLM training/evaluation with RLVR + governance.

## Feature Status

| Feature | Status | Notes |
|---------|--------|-------|
| FastAPI backend + JWT auth + RBAC | ✅ Complete | All routes enforce `require_role()` |
| Celery + Redis async job processing | ✅ Complete | Full lifecycle: queued→running→done/failed, retry w/ backoff |
| Next.js dashboard | ✅ Complete | Projects, models, evals, jobs, governance, incidents |
| Real verifiers (math, cyber defensive) | ✅ Complete | Math exact-match, vulnerability scanner, anti-hacking, calibration |
| Model endpoint integration | ✅ Complete | OpenAI, vLLM, generic endpoint clients |
| PDF export (system cards & eval reports) | ✅ Complete | Uses `reportlab` — real PDF generation with download |
| Prometheus/Grafana monitoring | ✅ Complete | `/metrics` endpoint, Prometheus + Grafana in docker-compose |
| Docker sandbox for code execution | ⚠️ Scaffolding | `sandbox.py` with Docker isolation exists, wired for `unit_test` jobs |
| gVisor (runsc) support | ⚠️ Planned | Compose config ready, `runtime: runsc` requires host install |
| Kubernetes Helm chart | ⚠️ Scaffolding | Templates for backend/worker/frontend; run `helm dep update` before install |
| RSP-style governance gates | ✅ v1 | DB-backed gates with admin approve/reject endpoint |
| Security incident tracking | ✅ Complete | Create, list, update (PATCH) incidents with RBAC |

## Quick Start

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env — at minimum set a real JWT_SECRET:
#   openssl rand -hex 32

# 2. Start all services
docker compose up --build

# 3. Full stack with monitoring + gVisor sandbox
docker compose -f docker-compose.gvisor.yml up --build
```

**URLs:**
- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin)
- Default login: `admin@local` / `admin123`

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend   │────▶│   Backend    │────▶│  PostgreSQL  │
│   (Next.js)  │     │  (FastAPI)   │     │              │
│   :3000      │     │  :8000       │     │  :5432       │
└──────────────┘     └──────┬───────┘     └──────────────┘
                           │
                    ┌──────▼───────┐     ┌──────────────┐
                    │    Redis     │◀───▶│   Worker     │
                    │   (Broker)   │     │  (Celery)    │
                    │   :6379      │     │              │
                    └──────────────┘     └──────┬───────┘
                                                │
                                         ┌──────▼───────┐
                                         │   Sandbox    │
                                         │  (Docker)    │
                                         └──────────────┘
```

### Components
- **Backend**: FastAPI + SQLAlchemy + JWT auth + RBAC on all routes
- **Worker**: Celery tasks with retry/backoff, idempotency checks
- **Verifiers**: Math exact-match, cyber defensive (vuln scanner, anti-hacking, calibration, patch verifier)
- **Model Client**: Unified `ModelClient.generate()` for OpenAI / vLLM / generic endpoints
- **Sandbox**: Docker container isolation with memory/cpu/network limits
- **Monitoring**: Prometheus metrics collection + Grafana dashboards

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/auth/register` | POST | — | Register new user |
| `/auth/login` | POST | — | Get JWT token |
| `/projects/` | GET/POST | All/Admin,Eng | List/create projects |
| `/models/` | GET/POST | All/Admin,Eng | List/create model registry entries |
| `/datasets/` | GET/POST | All/Admin,Eng | List/create datasets |
| `/jobs/` | GET/POST | All/Admin,Eng | List/create async jobs |
| `/governance/gates/{id}` | GET | All | View RSP gates for project |
| `/governance/gates/{id}/{gate}/approve` | POST | Admin | Approve/reject a gate |
| `/governance/audit-log/{id}` | GET | Admin,Auditor | View audit log |
| `/governance/compliance-report/{id}` | GET | Admin,Auditor | Generate compliance report |
| `/incidents/` | GET/POST | All/Admin,Eng | List/create incidents |
| `/incidents/{id}` | PATCH | Admin,Eng | Update incident status |
| `/reports/system-card/{id}` | GET | Admin,Eng,Aud | Markdown system card |
| `/reports/system-card/{id}/pdf` | GET | Admin,Eng,Aud | PDF system card download |
| `/reports/eval-report/{id}` | GET | Admin,Eng,Aud | Markdown eval report |
| `/reports/eval-report/{id}/pdf` | GET | Admin,Eng,Aud | PDF eval report download |
| `/metrics` | GET | — | Prometheus metrics |

## Deployment

### Docker Compose (Development)
```bash
docker compose -f docker-compose.override.yml up --build
```

### Docker Compose (Production)
```bash
docker compose -f docker-compose.prod.yml up -d
```

### Kubernetes (Helm)
```bash
cd helm/mythos-safe
helm dependency update
helm install mythos-safe . -f values.yaml
```

## Testing

```bash
cd backend
pip install -r requirements.txt
PYTHONPATH=$PWD pytest tests/ -v
```

## Documentation

- [Project Summary](PROJECT_SUMMARY.md)
- [Integration Status](INTEGRATION_STATUS.md)
