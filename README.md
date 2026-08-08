# D&D Character Companion

A web application for creating, managing, and using D&D 2024 characters during tabletop sessions.

## Status

Project under development.

Current milestone: V0.1 — Character Core.

## Requirements

- Python 3.9 or newer
- Git

## Backend setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the development dependencies:

```bash
python -m pip install -r backend/requirements-dev.txt
```

## Run the backend

```bash
cd backend
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