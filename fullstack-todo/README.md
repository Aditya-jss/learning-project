# Fullstack Todo (FastAPI + React)

Minimal CRUD starter with a FastAPI/SQLite backend and Vite/React frontend.

## Backend (FastAPI)

Requirements: Python 3.11+, `pip` (or `uv`), optional `venv`.

```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # or use uv
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Run tests:

```bash
cd backend
PYTHONPATH=. pytest
```

Endpoints live at `http://localhost:8000` with CRUD under `/api/todos/` and a health check at `/health`.

## Frontend (React + Vite)

Requirements: Node 18+ and npm.

```bash
cd frontend
npm install
npm run dev  # defaults to http://localhost:5173
```

The frontend proxies `/api` to `http://localhost:8000`. To point to a different backend, set `VITE_API_BASE_URL` in a `.env.local` file at `frontend/`.

## Project structure

- backend/app: FastAPI app, models, CRUD, router
- backend/tests: API tests with in-memory SQLite
- frontend/src: React app, API client, hooks, UI components

## Next steps

- Add auth (e.g., JWT) if you need user-specific todos
- Swap SQLite for Postgres/MySQL via SQLAlchemy URL changes
- Add CI to run `pytest` and `npm run build`
