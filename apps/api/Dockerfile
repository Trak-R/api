# Use Python 3.12 slim image
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y \
    ca-certificates \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Manifests first so dependency installs stay cached when only source changes.
COPY pyproject.toml uv.lock ./
COPY apps/api/pyproject.toml apps/api/pyproject.toml
COPY apps/persistence-worker/pyproject.toml apps/persistence-worker/pyproject.toml
COPY apps/anomaly-detector/pyproject.toml apps/anomaly-detector/pyproject.toml
COPY packages/core/pyproject.toml packages/core/pyproject.toml
COPY packages/identity/pyproject.toml packages/identity/pyproject.toml
COPY packages/documents/pyproject.toml packages/documents/pyproject.toml
COPY packages/alerts/pyproject.toml packages/alerts/pyproject.toml
COPY packages/aircraft/pyproject.toml packages/aircraft/pyproject.toml
COPY packages/weather/pyproject.toml packages/weather/pyproject.toml
COPY packages/anomalies/pyproject.toml packages/anomalies/pyproject.toml

RUN uv sync --frozen --package trakr-api --no-dev --no-install-project --no-install-workspace

COPY apps/api apps/api
COPY packages packages

RUN uv sync --frozen --package trakr-api --no-dev

EXPOSE 8000

CMD ["uvicorn", "trakr_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
