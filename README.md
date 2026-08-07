# EpsteinExplorer

> Credits: Erwin Lejeune — 2026-02-23

[![CI](https://github.com/guilyx/epsteinexplorer/actions/workflows/ci.yml/badge.svg)](https://github.com/guilyx/epsteinexplorer/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-19-61dafb)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Natural language research interface for the Epstein case files.**

A full-stack chatbot that lets you explore persons, documents, flight logs, and emails from the Epstein files using natural language — powered by [epsteinexposed](https://github.com/guilyx/epsteinexposed) and [smolagents](https://github.com/huggingface/smolagents).

[![EpsteinExplorer](https://raw.githubusercontent.com/guilyx/epsteinexplorer/main/promo/out/explorer-poster.png)](https://raw.githubusercontent.com/guilyx/epsteinexplorer/main/promo/out/explorer-16x9.mp4)

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

Run the Vite docs web app:

```bash
cd docs
nvm use || true
npm install
npm run dev
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

## The toolchain

This repository is one of four that share a data source and a design system:

| Repo | Role |
|---|---|
| [`epsteinexposed`](https://github.com/guilyx/epsteinexposed) | Python client for the public API |
| [`epsteinexposed-mcp`](https://github.com/guilyx/epsteinexposed-mcp) | MCP server — structured search |
| [`epstein-files-rag-mcp`](https://github.com/guilyx/epstein-files-rag-mcp) | MCP server — semantic search *(in development)* |
| [`epsteinexplorer`](https://github.com/guilyx/epsteinexplorer) | Natural-language chat app *(this repo)* |

A 20-second overview of how the four fit together:

[![Epstein Files toolchain](https://raw.githubusercontent.com/guilyx/epsteinexplorer/main/promo/out/suite-poster.png)](https://raw.githubusercontent.com/guilyx/epsteinexplorer/main/promo/out/suite-16x9.mp4)

Also related: [LinkedStein](https://github.com/guilyx/LinkedStein) — LinkedIn × Epstein files cross-reference tool.

## Design system

All four repositories share the **"Declassified"** visual language — a dark
archival palette with a single ember accent, monospace structure and Inter
prose. The canonical tokens live in [`brand/tokens.css`](brand/tokens.css)
and the rationale in [`brand/DESIGN.md`](brand/DESIGN.md); both files are
byte-identical across the four repos.

The app and its docs mirror those tokens into Tailwind via
`frontend/src/brand.css` and `docs/src/brand.css`. Verify they have not
drifted:

```bash
node brand/verify-tokens.mjs
```

## Promo assets

Silent, captioned promo videos are rendered from [`promo/`](promo/) —
animated HTML captured frame-by-frame through Chromium and encoded with
ffmpeg, so output is deterministic.

**Five clips:** one per tool, plus a **toolchain overview** (`suite-*`) that
presents all four together — the one to reach for when someone is meeting
the project for the first time.

```bash
cd promo && npm install && npm run render
```

Output lands in `promo/out/` as 16:9 and 1:1 MP4s plus poster stills. See
[`promo/README.md`](promo/README.md) for how the renderer works, and
[`LAUNCH.md`](LAUNCH.md) for how the clips map to each channel.

## Launch

[`LAUNCH.md`](LAUNCH.md) holds the go-to-market plan for the toolchain —
positioning, channel-by-channel copy, sequencing and risks.

## License

MIT — see [LICENSE](LICENSE).
