# Trakr

Monorepo for the Trakr API, background workers, and the shared domain library. Dependencies are managed with a [uv](https://docs.astral.sh/uv/) workspace and a single `uv.lock` at the repository root.

## Layout

```
.
├── pyproject.toml              # Workspace root
├── uv.lock
├── apps/
│   ├── api/                    # FastAPI application (trakr-api)
│   ├── persistence-worker/     # Placeholder worker
│   └── anomaly-detector/       # Placeholder worker
└── src/
    └── packages/
        ├── core/               # src/trakr_core
        ├── identity/           # src/identity
        ├── documents/          # src/documents
        ├── alerts/             # src/alerts
        ├── aircraft/           # src/aircraft
        ├── aircraft_telemetry/ # src/aircraft_telemetry
        ├── weather/            # src/weather
        └── anomalies/          # src/anomalies
```

`core` holds shared code: configuration, database, logging, Celery, security helpers, and base models, repositories, schemas, and services. Each domain package uses a src layout (`src/packages/aircraft/src/aircraft`) with `api`, `models`, `repository`, `schemas`, `services`, `tasks`, and `tests`. `trakr-api` depends on the domain packages and mounts their routers.

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- PostgreSQL >= 12
- Redis >= 7 (Celery broker)

## Setup

From the repository root:

```bash
uv sync --all-packages
```

Create a `.env` file in the repository root. The database name stays `vibeify` so an existing local database keeps working.

```env
API_V1_PREFIX=/api/v1
PROJECT_NAME=Trakr API
VERSION=0.1.0
DEBUG=false

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=vibeify

REDIS_URL=redis://localhost:6379/0
```

Create the database if it does not exist:

```sql
CREATE DATABASE vibeify;
```

Apply migrations:

```bash
uv run alembic -c apps/api/alembic.ini upgrade head
```

## Run

API (http://localhost:8000, docs at http://localhost:8000/docs):

```bash
uv run uvicorn trakr_api.main:app --reload
```

Celery worker and beat:

```bash
uv run celery -A trakr_api.celery worker --loglevel=info
uv run celery -A trakr_api.celery beat --loglevel=info
```

Placeholder workers:

```bash
uv run trakr-persistence-worker
uv run trakr-anomaly-detector
```

### Docker Compose

Build context is the repository root so the image can install `trakr-core` with the API.

```bash
docker compose up -d
```

Postgres, Redis, and MinIO data volumes are unchanged from the previous Compose file.

## Development

```bash
uv run pytest
uv run ruff check .
uv run ruff format .
```

Add a dependency to one member:

```bash
uv add --package trakr-api <package>
```
