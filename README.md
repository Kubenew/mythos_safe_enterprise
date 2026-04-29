# Mythos Safe Enterprise

**Enterprise platform for safe LLM evaluation, RLVR training, and defensive cybersecurity governance.**

Built as a practical implementation inspired by Anthropic’s Claude Mythos Preview System Card and Project Glasswing.

---

## 🎯 Overview

Mythos Safe Enterprise is a full-stack platform designed to safely evaluate and govern frontier AI models with a strong focus on **defensive cybersecurity capabilities**.

It enables:
- Rigorous testing of model outputs for security vulnerabilities
- Strict enforcement of safety boundaries (no offensive or harmful content)
- Support for **RLVR** (Reinforcement Learning with Verifiable Rewards)
- Full auditability and governance features
- Secure execution using gVisor sandboxing

The system directly addresses key risks identified in the Mythos Preview System Card: reward hacking, reckless actions, over-engineering, poor calibration, and dual-use risks.

---

## ✨ Key Features

### Defensive Cyber Evaluation Engine
- **VulnerabilityScannerVerifier**: Detects SQL injection, XSS, command injection, path traversal, etc.
- **CyberAntiHackingVerifier**: Hard safety gate — blocks exploits, payloads, and reward hacking attempts
- **OverEngineeringDetector**: Prevents overly complex or poorly calibrated responses
- **PatchVerifier**: Validates safe, minimal, and effective remediation patches
- **Composite Reward System**: Weighted scoring combining accuracy, safety, calibration, and patching quality

### Technical Stack
- **Backend**: FastAPI + SQLAlchemy + Alembic
- **Async Layer**: Celery + Redis
- **Frontend**: Next.js with interactive evaluation card
- **Security**: gVisor-protected sandbox
- **Deployment**: Docker Compose (dev + prod), Traefik + Let's Encrypt SSL
- **Monitoring**: Flower (Celery dashboard)

### Safety Philosophy
- Strictly **defensive-only** — offensive content is automatically rejected with `composite_reward = 0.0`
- Full audit trail for every evaluation
- Designed for responsible scaling and high-stakes AI governance

---

## 📁 Project Structure

```bash
mythos_safe_enterprise/
├── backend/
│   ├── app/
│   │   ├── verifiers/cyber_defensive/     # Core safety verifiers
│   │   ├── services/verification_service.py
│   │   ├── schemas/verification.py
│   │   ├── models/evaluation.py
│   │   ├── api/endpoints/evaluation.py
│   │   └── main.py
│   ├── worker/
│   │   ├── worker.py
│   │   └── tasks.py
│   └── requirements.txt
├── frontend/                          # Next.js dashboard
├── docker/                            # Sandbox configuration
├── test_cases/                        # Test code samples
├── docker-compose.yml
├── docker-compose.override.yml
├── docker-compose.prod.yml
├── docker-compose.gvisor.yml
├── traefik.yml
├── .env.example
├── GETTING_STARTED.md
├── DEPLOYMENT.md
└── ARCHITECTURE.md
```

## 🚀 Quick Start (Local Development)

### 1. Clone & Setup
```bash
git clone https://github.com/Kubenew/mythos_safe_enterprise.git
cd mythos_safe_enterprise
cp .env.example .env
# Edit .env with your settings
```

### 2. Start Services
```bash
docker compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

### 3. Run Database Migrations
```bash
docker compose exec api alembic upgrade head
```

### 4. Test the System
```bash
# Run curl test
./test_curl.sh

# Or use the test script
python test_cyber_evaluation.py
```

### 5. Access the Services
- **API Documentation**: http://localhost:8000/docs
- **Celery Monitor (Flower)**: http://localhost:5555
- **Frontend Dashboard**: http://localhost:3000 (if running)

---

## 🛠️ Usage Example

`POST /api/evaluation/cyber-defensive`

```json
{
  "prompt": "Analyze this code for security vulnerabilities and suggest safe fixes.",
  "response": "I found a SQL injection vulnerability because user input is directly concatenated...",
  "target_code": "SELECT * FROM users WHERE id = '" + user_input + "'"
}
```
The response includes `composite_reward`, detailed verifier outputs, and safety status.

---

## 🏗️ Architecture
The platform follows a clean layered architecture:

- **Frontend** → Calls API
- **API Layer** → FastAPI + VerificationService
- **Safety Core** → Modular cyber_defensive verifiers
- **Async Layer** → Celery workers for heavy evaluations
- **Storage** → PostgreSQL with full audit trail
- **Isolation** → gVisor sandbox

*(See `ARCHITECTURE.md` for the detailed Mermaid diagram.)*

---

## 📋 Production Deployment
Use the production configuration:
```bash
docker compose -f docker-compose.prod.yml up -d
```

**Production Features:**
- Traefik reverse proxy with automatic SSL
- gVisor-enhanced sandbox for maximum isolation
- Scalable Celery workers
- Structured logging and monitoring

See `PRODUCTION_DEPLOYMENT_CHECKLIST.md` and `DEPLOYMENT.md` for detailed instructions.

---

## 🧪 Testing
```bash
pytest backend/tests/ -v
```

---

## 🛡️ Safety & Governance
- All evaluations are defensive-only
- Harmful or offensive outputs are automatically rejected
- Every evaluation is logged with full context for auditability
- Designed to support responsible scaling policies

---

## 📄 Additional Documentation
- `GETTING_STARTED.md` — Quick start guide
- `DEPLOYMENT.md` — Deployment instructions
- `ARCHITECTURE.md` — System architecture
- `PRODUCTION_DEPLOYMENT_CHECKLIST.md` — Production readiness checklist

---

## 🤝 Contributing
Contributions are welcome. Please ensure changes maintain the strict defensive-only policy and pass all safety tests.

## 📜 License
MIT License — see the LICENSE file for details.

*Mythos Safe Enterprise — Building safer, more capable AI systems through rigorous defensive evaluation and responsible governance.*
