# Architecture

> Credits: Erwin Lejeune - 2026-02-24

## System

```text
Frontend (React/Vite) -> Backend (FastAPI) -> Agent (smolagents/LiteLLM) -> epsteinexposed
                                   |
                                   -> PostgreSQL (users, conversations, messages)
```

## Components

- `frontend/`: single-page chat UI
- `backend/`: API routes, persistence, SSE streaming
- `agent/`: tool-enabled research agent wrapper
- `docs/`: VitePress documentation

## Data flow

1. User sends message from the frontend.
2. Backend resolves anonymous user identity (IP hash + optional fingerprint).
3. Agent executes tool-assisted reasoning against `epsteinexposed`.
4. Streamed response is returned to the client and persisted.
