# D&D Character Companion

A web application for creating, managing, and using D&D 2024 characters during tabletop sessions.

## Status

Project under development.

Current milestone: V0.1 — Character Core.

## Requirements

- Git
- Python 3.9 or newer
- Docker with Docker Compose

## Backend setup

Create the local environment file:

```bash
cp .env.example .env
```

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the development dependencies:

```bash
python -m pip install -r backend/requirements-dev.txt
```

## Start the database

```bash
docker compose up -d database
docker compose ps
```

PostgreSQL is exposed locally on port `5433`.

Stop the database without deleting its data:

```bash
docker compose down
```

## Run database migrations

From the `backend` directory:

```bash
alembic upgrade head
```

Show the current migration:

```bash
alembic current
```

## Run the backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- Health check: <http://127.0.0.1:8000/health>
- Interactive documentation: <http://127.0.0.1:8000/docs>

Press `Ctrl+C` to stop the server.

## Run the tests

From the `backend` directory:

```bash
python -m pytest
```

## Project scope

See [PROJECT_SCOPE.md](PROJECT_SCOPE.md) for the complete product specification.