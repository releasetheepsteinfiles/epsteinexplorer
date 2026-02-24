# EpsteinExplorer

> Credits: Erwin Lejeune — 2026-02-23

[![CI](https://github.com/guilyx/epsteinexplorer/actions/workflows/ci.yml/badge.svg)](https://github.com/guilyx/epsteinexplorer/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-19-61dafb)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Natural language research interface for the Epstein case files.**

A full-stack chatbot that lets you explore persons, documents, flight logs, and emails from the Epstein files using natural language — powered by [epsteinexposed](https://github.com/guilyx/epsteinexposed) and [smolagents](https://github.com/huggingface/smolagents).

> **Disclaimer:** Inclusion in the Epstein Exposed database does not imply guilt or wrongdoing. All data is derived from publicly released government records, court filings, and verified reporting.

## Architecture

```
┌─────────────┐    SSE     ┌──────────────┐    SQL     ┌──────────┐
│   Frontend   │◄──────────►│   Backend    │◄──────────►│ Postgres │
│  React/Vite  │   /api/*   │   FastAPI    │            │   16     │
│  Tailwind    │            │              │            │          │
└─────────────┘            │  ┌─────────┐ │            └──────────┘
                           │  │  Agent  │ │
                           │  │smolagent│ │
                           │  └────┬────┘ │
                           │       │      │
                           └───────┼──────┘
                                   │
                           ┌───────▼──────┐
                           │epsteinexposed│
                           │  (PyPI pkg)  │
                           └──────────────┘
```

| Layer | Stack |
|---|---|
| **Frontend** | React 19, Vite 6, Tailwind CSS 4, TypeScript |
| **Backend** | FastAPI, SQLAlchemy 2.0 async, Alembic, SSE |
| **Agent** | smolagents ToolCallingAgent, LiteLLM |
| **Data** | [epsteinexposed](https://pypi.org/project/epsteinexposed/) v0.2.0 |
| **Database** | PostgreSQL 16 |

## Features

- Single-page chatbot with suggestion prompts
- LLM-powered agent with 5 Epstein file tools (persons, documents, flights, cross-search)
- Anonymous user tracking (IP hash + browser fingerprint)
- Conversation persistence in PostgreSQL
- SSE streaming for real-time responses
- Cyberpunk modern dark theme

## Quick Start

### Docker Compose (recommended)

```bash
cp .env.example .env
# Edit .env → add your OPENROUTER_API_KEY

docker compose up --build

# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API docs: http://localhost:8000/docs
```

### Local Development

**Backend:**

```bash
cd backend
pip install -e ".[dev]"
cp ../.env.example ../.env  # add your OPENROUTER_API_KEY

# Start Postgres (or use docker compose up db)
alembic upgrade head
uvicorn app.main:app --reload
```

**Frontend:**

```bash
cd frontend
npm ci
npm run dev
# Opens on http://localhost:5173, proxies /api to backend
```

## Documentation

Run the VitePress docs site:

```bash
cd docs
npm install
npm run docs:dev
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://...@localhost:5432/epsteinexplorer` | Async SQLAlchemy DB URL |
| `LLM_MODEL` | `openrouter/google/gemini-2.0-flash-001` | LiteLLM model identifier (any [OpenRouter model](https://openrouter.ai/models)) |
| `OPENROUTER_API_KEY` | | Your OpenRouter API key |
| `CORS_ORIGINS` | `http://localhost:5173,http://localhost:3000` | Allowed CORS origins |

## Agent Tools

The smolagents `ToolCallingAgent` has access to these tools via `epsteinexposed`:

| Tool | Description |
|---|---|
| `search_persons` | Search/filter persons of interest |
| `get_person_detail` | Full bio, aliases, stats for a person |
| `search_documents` | Full-text document search |
| `search_flights` | Flight log search |
| `cross_search` | Search across documents and emails |

## Related Projects

- [epsteinexposed](https://github.com/guilyx/epsteinexposed) — Python client for the Epstein Exposed API
- [epsteinexposed-mcp](https://github.com/guilyx/epsteinexposed-mcp) — MCP server wrapping the same API
- [LinkedStein](https://github.com/guilyx/LinkedStein) — LinkedIn x Epstein files cross-reference tool

## License

MIT — see [LICENSE](LICENSE).
