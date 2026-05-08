# Mythos Safe Enterprise

[![PyPI - Version](https://img.shields.io/pypi/v/mythos-safe-enterprise)](https://pypi.org/project/mythos-safe-enterprise/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mythos-safe-enterprise)](https://pypi.org/project/mythos-safe-enterprise/)
[![PyPI - License](https://img.shields.io/pypi/l/mythos-safe-enterprise)](https://github.com/Kubenew/mythos_safe_enterprise/blob/main/LICENSE)
[![Downloads](https://pepy.tech/badge/mythos-safe-enterprise)](https://pepy.tech/project/mythos-safe-enterprise)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/Kubenew/mythos_safe_enterprise)](https://github.com/Kubenew/mythos_safe_enterprise)

**Enterprise platform for safe LLM evaluation and defensive cybersecurity governance.**

Built to support the safe development of frontier AI models (Mythos++ class), inspired by Anthropic’s Claude Mythos Preview System Card.

---

## ✨ Features

- **Defensive Cyber Evaluation Engine** with multiple specialized verifiers
- **Strict Safety Gates** — automatic rejection of offensive or harmful content
- **Composite Reward Scoring** combining accuracy, safety, calibration, and patching quality
- **Full Audit Trail** — all evaluations stored with detailed results
- **Secure Sandboxing** using gVisor
- **Scalable Async Processing** via Celery + Redis
- **Production-ready deployment** with Traefik + Let's Encrypt SSL

### Core Verifiers
- `VulnerabilityScannerVerifier`
- `CyberAntiHackingVerifier`
- `OverEngineeringDetector`
- `PatchVerifier`

---

## 🚀 Quick Start (Development)

```bash
git clone https://github.com/Kubenew/mythos_safe_enterprise.git
cd mythos_safe_enterprise

cp .env.example .env
# Edit .env with your settings

docker compose -f docker-compose.yml -f docker-compose.override.yml up -d

# Run migrations
docker compose exec api alembic upgrade head

# Test the system
./test_curl.sh

Access:

API Docs: http://localhost:8000/docs
Celery Flower: http://localhost:5555


🏗️ Production Deployment
Bashdocker compose -f docker-compose.prod.yml up -d
See PRODUCTION_DEPLOYMENT_CHECKLIST.md for detailed steps.

📁 Project Structure

backend/app/verifiers/cyber_defensive/ — Core safety logic
backend/app/services/verification_service.py — Main evaluation service
backend/app/worker/ — Celery tasks
docker-compose.*.yml — Multiple deployment profiles
test_cases/ — Sample vulnerable code for testing


🛡️ Safety Philosophy
All evaluations are strictly defensive. Any attempt to generate exploits, payloads, or harmful content results in immediate rejection (composite_reward = 0.0).
This platform aims to help develop AI systems that strengthen defenders while minimizing dual-use risks.

📄 Documentation

GETTING_STARTED.md
DEPLOYMENT.md
ARCHITECTURE.md
PRODUCTION_DEPLOYMENT_CHECKLIST.md


Status: Production-ready scaffold with strong defensive cyber capabilities.
Built with responsibility, transparency, and safety at the core.