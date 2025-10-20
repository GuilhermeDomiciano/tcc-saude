# Repository Guidelines

## Project Structure & Module Organization
- `backend/`: FastAPI + SQLModel API. Main entry at `backend/main.py`. Config via env: `DATABASE_URL`, `UPLOAD_DIR`, `ALLOWED_ORIGINS`.
- `frontend/`: React + Vite + TypeScript app. Source in `frontend/src`, static in `frontend/public`.
- `app_data/uploads`: Local storage for uploaded files during development.
- `docker-compose.yml`: Orchestrates `api`, `web`, and `redis`. Uses `.env` for shared variables (e.g., `VITE_API_BASE`).

## Build, Test, and Development
- Docker (recommended): `docker compose up --build` — builds and runs API, web, and Redis.
- Backend local dev: `cd backend && pip install -r requirements.txt && uvicorn main:app --reload --host 0.0.0.0 --port 8000`
- Frontend local dev: `cd frontend && npm i && npm run dev` (Vite dev server on `http://localhost:5173`).
- Frontend build/preview: `npm run build` then `npm run preview`.
- Lint (frontend): `npm run lint`.

## Coding Style & Naming
- Python: follow PEP 8, 4‑space indentation, type hints required for public functions. Prefer Pydantic v2/SQLModel models for I/O and persistence.
- React/TS: components in `PascalCase`, files `ComponentName.tsx`; hooks `useThing.ts`. Avoid default exports for components.
- Keep modules small and cohesive; colocate feature-specific code under a directory in `src`.

## Testing Guidelines
- Currently no formal test suite. When contributing:
  - Backend: add `pytest` tests under `backend/tests/` named `test_*.py`.
  - Frontend: use Vitest/Jest style `*.test.ts(x)` under `frontend/src/` near code.
- Aim for meaningful coverage of routes, data parsing, and UI states; target ≥80% where practical.

## Commit & Pull Request Guidelines
- Use Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`.
- PRs must include: clear description, linked issues, steps to validate, and screenshots/GIFs for UI.
- Before opening a PR: run `npm run lint` (frontend) and a quick manual pass on `http://localhost:5173` and `/health` on the API.

## Security & Config Tips
- Do not commit secrets. Store credentials in `.env` and set `DATABASE_URL` explicitly when not using a local DB.
- Keep `ALLOWED_ORIGINS` narrowed for deployments. Ensure `VITE_API_BASE` points to the API URL.
