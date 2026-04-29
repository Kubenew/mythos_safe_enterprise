# Model Registry

## How to Use

### 1. Start the Stack

```bash
# Basic setup
cp .env.example .env
docker compose up --build

# With gVisor sandbox (requires gVisor installed)
docker compose -f docker-compose.gvisor.yml up --build
```

### 2. Register a Model

```bash
# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@local", "password": "admin123"}'

# Register model
curl -X POST http://localhost:8000/models/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "name": "my-llm-model",
    "version": "1.0",
    "endpoint": "http://localhost:8000/v1"
  }'
```

### 3. Run Evaluation with Real Model

```bash
# Run math evaluation with model endpoint
curl -X POST http://localhost:8000/jobs/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "type": "eval",
    "input": {
      "suite": "math_mini",
      "model_endpoint": "https://api.openai.com/v1",
      "api_key": "sk-your-key",
      "model_name": "gpt-3.5-turbo"
    }
  }'
```

### 4. Check Results

```bash
# Get job status
curl http://localhost:8000/jobs/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get system card
curl http://localhost:8000/reports/system-card/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## gVisor Setup (Optional but Recommended)

gVisor provides stronger isolation than standard Docker:

### Install gVisor (Linux)

```bash
# Download and install
curl -fsSL https://gvisor.dev/archive/2024.01.08/runsc | sudo tee /usr/local/bin/runsc
sudo chmod +x /usr/local/bin/runsc

# Configure Docker
sudo runsc install
sudo systemctl restart docker
```

### Verify Installation

```bash
docker run --runtime=runsc --rm hello-world
```

## Sandbox Features

The sandbox (`worker/worker/sandbox.py`) provides:

- ✅ Resource limits (128MB RAM, 0.5 CPU)
- ✅ Network isolation (`--network=none`)
- ✅ Read-only filesystem
- ✅ Timeout protection (30s default)
- ✅ Docker-based isolation

With gVisor (`--runtime=runsc`):

- ✅ Kernel-level isolation
- ✅ Stronger security guarantees
- ✅ Defense against container escape

## Current Status

| Feature | Status |
|---------|--------|
| Backend API | ✅ Ready |
| Model Client | ✅ Integrated |
| Frontend Pages | ✅ Complete |
| Sandbox (Docker) | ✅ Ready |
| Sandbox (gVisor) | ⚠️ Needs install |
| Real Evals | ✅ Works with endpoints |
