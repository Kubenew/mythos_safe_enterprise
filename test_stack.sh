#!/bin/bash
# Test Mythos-Safe Full Stack

echo "=== Mythos-Safe Enterprise MVP - Stack Test ==="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running. Please start Docker first."
    exit 1
fi

echo "1. Checking project structure..."
if [ ! -f "docker-compose.yml" ]; then
    echo "ERROR: docker-compose.yml not found"
    exit 1
fi
echo "   ✓ docker-compose.yml found"

if [ ! -f ".env" ]; then
    echo "   Creating .env from .env.example..."
    cp .env.example .env
fi
echo "   ✓ .env file ready"

echo ""
echo "2. Building and starting services..."
docker compose build
docker compose up -d

echo ""
echo "3. Waiting for services to be ready..."
sleep 10

echo ""
echo "4. Testing backend API..."
HEALTH_CHECK=$(curl -s http://localhost:8000/ | grep -o '"status":"ok"')
if [ -z "$HEALTH_CHECK" ]; then
    echo "   ✗ Backend not responding"
else
    echo "   ✓ Backend is healthy"
fi

echo ""
echo "5. Testing authentication..."
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@local","password":"admin123"}' | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "   ✗ Authentication failed"
else
    echo "   ✓ Authentication successful"
fi

echo ""
echo "6. Testing project creation..."
CREATE_PROJECT=$(curl -s -X POST http://localhost:8000/projects/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Project","description":"Testing the full stack"}')

PROJECT_ID=$(echo $CREATE_PROJECT | grep -o '"id":[0-9]*' | cut -d':' -f2)
if [ -z "$PROJECT_ID" ]; then
    echo "   ✗ Project creation failed"
else
    echo "   ✓ Project created (ID: $PROJECT_ID)"
fi

echo ""
echo "7. Testing job creation..."
CREATE_JOB=$(curl -s -X POST http://localhost:8000/jobs/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"project_id\":$PROJECT_ID,\"type\":\"math_eval\",\"input\":{\"suite\":\"math_mini\"}}")

JOB_ID=$(echo $CREATE_JOB | grep -o '"id":[0-9]*' | cut -d':' -f2)
if [ -z "$JOB_ID" ]; then
    echo "   ✗ Job creation failed"
else
    echo "   ✓ Job created (ID: $JOB_ID)"
fi

echo ""
echo "8. Waiting for job to complete..."
sleep 15

echo ""
echo "9. Checking job status..."
JOB_STATUS=$(curl -s http://localhost:8000/jobs/ \
  -H "Authorization: Bearer $TOKEN" | grep -o '"status":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ "$JOB_STATUS" = "done" ]; then
    echo "   ✓ Job completed successfully"
    echo ""
    echo "10. Fetching evaluation results..."
    curl -s http://localhost:8000/jobs/ \
      -H "Authorization: Bearer $TOKEN" | python -m json.tool | head -30
else
    echo "   ⚠ Job status: $JOB_STATUS (might still be running)"
fi

echo ""
echo "=== Test Complete ==="
echo ""
echo "Access points:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000/docs"
echo "  System Card: http://localhost:8000/reports/system-card/$PROJECT_ID"
echo ""
echo "To stop: docker compose down"
