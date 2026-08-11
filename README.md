# D&D Character Companion

A web application for creating, managing, and using D&D 2024 characters during tabletop sessions.

## Status

Project under development.

Current milestone: V0.1 — Character Core.

## Requirements

- Git
- Python 3.9 or newer
- Docker with Docker Compose

## Docker quick start

Create the local environment file:

```bash
cp .env.example .env
```

Generate a JWT secret:

```bash
openssl rand -hex 32
```

Set the generated value as `JWT_SECRET_KEY` in `.env`.

Build and start the complete development stack:

```bash
docker compose up --build -d
docker compose ps
```

Available services:

- Frontend: <http://localhost:5173>
- API documentation: <http://localhost:8000/docs>
- API health check: <http://localhost:8000/health>
- PostgreSQL: `localhost:5433`

View logs:

```bash
docker compose logs -f
```

Stop the stack without deleting database data:

```bash
docker compose down
```

Do not use `docker compose down -v` unless you intentionally want to delete the PostgreSQL volume.

## Backend setup

Create the local environment file:

```bash
cp .env.example .env
```

Generate a local JWT secret:

```bash
openssl rand -hex 32
```

Set the generated value as `JWT_SECRET_KEY` in `.env`. Never commit the local `.env` file.

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the development dependencies:

```bash
python -m pip install -r backend/requirements-dev.txt
```

## Frontend setup

Install the frontend dependencies:

```bash
cd frontend
npm install
```

Optionally create a local frontend environment file:

```bash
cp .env.example .env
```

## Run the frontend

From the `frontend` directory:

```bash
npm run dev
```

The web application will be available at:

- <http://localhost:5173>

The backend must also be running at `http://127.0.0.1:8000`.

## Frontend checks

From the `frontend` directory:

```bash
npm test
npm run lint
npm run build
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

## Current frontend features

- JWT sign-in and sign-out;
- protected character routes;
- authenticated character list;
- Paladin character creation;
- character dashboard with derived statistics;
- responsive Material UI layout;
- route-based code splitting;
- automated tests for login, list, creation, and detail flows.
- account registration with automatic sign-in;
- expired-session redirection;
- character editing with a reusable form;
- character deletion with explicit confirmation;

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

## Authentication

Available endpoints:

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`

Protected endpoints expect an access token:

```text
Authorization: Bearer <access-token>
JWT access tokens expire after 30 minutes by default.
```

## Character API

All character endpoints require Bearer authentication.

Available endpoints:

- `POST /api/characters`
- `GET /api/characters`
- `GET /api/characters/{character_id}`
- `PUT /api/characters/{character_id}`
- `DELETE /api/characters/{character_id}`

Character responses include calculated values such as:

- ability modifiers;
- proficiency bonus;
- saving throw modifiers;
- skill modifiers;
- initiative;
- passive perception;
- spell attack modifier;
- spell save DC.

Character queries are always restricted to the authenticated owner.

## Run the tests

From the `backend` directory:

```bash
python -m pytest
```

## Project scope

See [PROJECT_SCOPE.md](PROJECT_SCOPE.md) for the complete product specification.