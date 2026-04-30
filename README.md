# Mythos Safe Enterprise

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