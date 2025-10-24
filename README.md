# Review Monitoring & Management Stack

This repository provides a proof-of-concept stack for monitoring public reviews,
normalizing them into a shared schema, running lightweight analysis hooks, and
testing response workflows via a safe simulation endpoint. The backend is built
with FastAPI and SQLite (swap to Postgres for production). A frontend scaffold
folder is included for building a dashboard in React or any SPA framework.

## Features

- **Collectors** – Use official APIs when available. Read-only connectors for
  Yelp and Trustpilot demonstrate how to fetch public review data while
  respecting robots.txt and rate limits. The Google connector is a stub awaiting
  Business Profile API credentials.
- **Normalization** – Reviews are mapped into a canonical schema so all
  platforms appear the same downstream.
- **Storage** – SQLAlchemy models default to SQLite. Bring your own database by
  overriding `DATABASE_URL`.
- **Analysis Hooks** – The structure is ready for LLM or rules-based tagging and
  sentiment analysis. Extend the model and tasks to queue additional work.
- **Response Simulation** – `/simulate/post` lets you exercise the response flow
  without touching real review sites.
- **Scheduler** – APScheduler powers background polling tasks. The provided job
  periodically fetches demo Yelp data.

## Project Structure

```
backend/
  app/
    connectors/
    db.py
    main.py
    models.py
    schemas.py
    simulate.py
    tasks.py
    utils.py
  requirements.txt
frontend/
  README.md (create your dashboard here)
docker-compose.yml
.env.example
```

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --app-dir backend
```

Then browse to <http://localhost:8000/docs> to interact with the API.

## Docker

```bash
docker-compose up --build
```

## Environment Variables

Copy `.env.example` to `.env` and adjust values:

- `DATABASE_URL` – SQLAlchemy connection string.
- `GOOGLE_API_KEY` – Credentials for the Google Business Profile API (if used).
- `RATE_LIMIT_REQUESTS_PER_MIN` – Optional knob for custom rate limiting logic.

## Frontend Scaffold

The `frontend/` directory is intentionally empty aside from this placeholder.
Use Vite, Create React App, or your preferred tooling to build a dashboard that
consumes the backend endpoints. Wire up `/simulate/post` for safe posting tests
before integrating any official response APIs.
