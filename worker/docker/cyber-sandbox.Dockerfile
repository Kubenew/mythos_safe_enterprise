# Docker sandbox for Mythos-Safe defensive cyber verification
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 sandboxuser
USER sandboxuser
WORKDIR /sandbox

COPY --chown=sandboxuser requirements-sandbox.txt .
RUN pip install --user --no-cache-dir -r requirements-sandbox.txt

ENV PYTHONUNBUFFERED=1
ENV PATH="/home/sandboxuser/.local/bin:${PATH}"

CMD ["echo", "Mythos-Safe Defensive Cyber Sandbox initialized."]
