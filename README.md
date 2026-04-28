# Mythos-Safe Enterprise MVP

Enterprise-grade AI platform for safe LLM training/evaluation with RLVR + governance.

## Features

- ✅ FastAPI backend with JWT auth + RBAC
- ✅ Celery + Redis async job processing
- ✅ Next.js dashboard (projects, models, evals, jobs, governance)
- ✅ Real verifiers from Mythos-Safe blueprint
- ✅ Model endpoint integration (OpenAI, vLLM)
- ✅ PDF export for system cards & eval reports
- ✅ Prometheus/Grafana monitoring
- ✅ Docker sandbox with gVisor support
- ✅ Kubernetes Helm chart
- ✅ RSP-style governance gates
- ✅ Security incident tracking

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

Frontend: http://localhost:3000
Backend API: http://localhost:8000/docs
Default login: admin@local / admin123

## Architecture

- **Backend**: FastAPI + PostgreSQL + JWT auth
- **Worker**: Celery + Redis for async jobs
- **Frontend**: Next.js dashboard
- **Verifiers**: Math, unit tests, cyber defensive (from blueprint)
- **Sandbox**: Docker/gVisor for secure code execution

## Documentation

- [Integration Status](INTEGRATION_STATUS.md)
- [Final Status](FINAL_STATUS.md)
- [Helm Chart](HELM_README.md)
- [Model Registry](MODEL_REGISTRY.md)
