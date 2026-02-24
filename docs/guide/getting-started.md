# Getting Started

> Credits: Erwin Lejeune - 2026-02-24

## Requirements

- Docker + Docker Compose
- Node.js 22+ (for docs local dev)

## Run the app

```bash
cp .env.example .env
docker compose up --build
```

App URLs:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Agent: `http://localhost:8001`

## Run docs site

```bash
cd docs
npm install
npm run docs:dev
```

Docs URL:

- `http://localhost:5173`
