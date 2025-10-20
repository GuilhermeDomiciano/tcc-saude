# Backend Architecture Guide

This backend is organized for clarity, testability, and incremental growth. Each folder separates a concern; start small and extend as features mature.

- app/core: Application-wide setup and configuration. Provides settings (env-driven) and shared app wiring.
- app/api: HTTP-layer only. Routers, request/response handling, and dependency wiring. No business logic here.
- app/api/routes: Route modules grouped by domain (e.g., health). Each file registers endpoints on a router.
- app/models: Persistence-layer entities (e.g., SQLModel/ORM) — define tables and relations here when a DB is enabled.
- app/schemas: Pydantic models for request/response payloads (DTOs). Keep them separate from persistence models.
- app/services: Business logic and integrations (e.g., storage, email, background jobs). Stateless and reusable.
- app/repositories: Data-access abstractions. Encapsulate queries and persistence details.
- app/utils: Small, generic utilities (pure functions, helpers).
- app/workers: Background tasks (e.g., RQ/celery). Keep task definitions and queues here.

Conventions
- Keep route handlers thin; delegate to services. 
- Avoid importing from api into services/repositories (one-way dependency).
- Add unit tests colocated by feature or under tests/ (not included yet).

Bootstrapping
- main.py creates the FastAPI app, loads CORS from settings, mounts routers from app/api, and leaves stubs for DB and storage initialization for future work.

Extend safely
- Add new features by creating a schema → service → repository → route. Keep changes minimal and cohesive.
