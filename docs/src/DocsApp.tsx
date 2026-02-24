// Credits: Erwin Lejeune — 2026-02-24
const toc = [
  ["overview", "Overview"],
  ["conceptual-model", "Conceptual Model"],
  ["design-principles", "Design Principles"],
  ["architecture", "Architecture"],
  ["data-flow", "Data Flow"],
  ["persistence-model", "Persistence Model"],
  ["api-reference", "API Reference"],
  ["agent-tools", "Agent Tools"],
  ["dos-donts", "Do / Don't"],
  ["why-what-not", "Why & What Not To Do"],
  ["quick-start", "Quick Start"],
  ["operations", "Operations Runbook"],
  ["troubleshooting", "Troubleshooting"],
  ["configuration", "Configuration"],
  ["security", "Security Notes"],
  ["observability", "Observability & Caching"],
  ["contributing", "Contributing"],
];

const endpoints = [
  {
    method: "GET",
    path: "/api/health",
    request: "None",
    response: '{ "status": "ok" }',
    notes: "Liveness endpoint for probes/monitoring.",
  },
  {
    method: "POST",
    path: "/api/chat",
    request:
      '{ "message": "string", "conversation_id": "uuid?", "fingerprint": "string?", "session_id": "string?" }',
    response:
      'SSE stream of JSON events: {"type":"message","content":"..."}, {"type":"error","content":"..."}, {"type":"done","conversation_id":"uuid"}',
    notes:
      "Main chat endpoint. Persists user + messages + request/tool/API logs and uses DB cache for tool calls.",
  },
  {
    method: "GET",
    path: "/docs",
    request: "None",
    response: "Swagger UI",
    notes: "Auto-generated OpenAPI docs from FastAPI.",
  },
];

const envVars = [
  [
    "DATABASE_URL",
    "postgresql+asyncpg://explorer:explorer@localhost:5432/epsteinexplorer",
    "Primary async SQLAlchemy connection string.",
  ],
  [
    "OPENROUTER_API_KEY",
    "(required for agent)",
    "API key for OpenRouter via LiteLLM.",
  ],
  [
    "LLM_MODEL",
    "openrouter/google/gemini-2.0-flash-001",
    "Default model routed by LiteLLM.",
  ],
  [
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:3000",
    "Comma-separated allowed origins.",
  ],
  [
    "EPSTEIN_CACHE_TTL_SECONDS",
    "3600",
    "TTL for DB-backed epsteinexposed response cache.",
  ],
];

const tools = [
  ["search_persons", "Search persons by name/category."],
  ["get_person_detail", "Fetch detailed person profile by slug."],
  ["search_documents", "Full-text search across documents."],
  ["search_flights", "Filter flight log records by passenger/route/year."],
  ["cross_search", "Cross-search documents + emails in one request."],
];

const conceptualModelRows = [
  [
    "Anonymous User",
    "Identity represented by `ip_hash` and optional `fingerprint`; no auth account is required.",
  ],
  [
    "Conversation",
    "Logical thread for a user session; links all request/response messages and telemetry.",
  ],
  [
    "Agent Execution",
    "Single run of `ToolCallingAgent` for one prompt; may trigger multiple tool calls.",
  ],
  [
    "Tool Call",
    "Invocation of one domain function (`search_persons`, etc.) with typed arguments.",
  ],
  [
    "Downstream API Call",
    "Call through `epsteinexposed` package to remote data API, possibly bypassed by cache hit.",
  ],
];

const designPrinciples = [
  "Auditability first: every meaningful request/tool/downstream action is persisted for traceability.",
  "Deterministic caching: endpoint + normalized params define cache key and reuse behavior.",
  "Bounded complexity: one chat endpoint coordinates orchestration; domain logic remains in services/tools.",
  "Operational clarity: failures surface as structured SSE error events and are persisted in logs.",
  "No hidden auth assumptions: system is designed for anonymous usage with privacy-aware identifiers.",
];

const architectureDiagram = `
┌───────────────────── Client Layer ─────────────────────┐
│ Browser (React SPA)                                    │
│ - sends POST /api/chat                                 │
│ - consumes SSE message/error/done events               │
└─────────────────────────────┬───────────────────────────┘
                              │
                              ▼
┌───────────────────── API Layer (FastAPI) ──────────────┐
│ /api/chat router                                        │
│ - resolve anonymous user (ip_hash + fingerprint)        │
│ - create/load conversation                              │
│ - persist user message                                  │
│ - run agent in executor                                 │
│ - stream assistant result                               │
└─────────────────────────────┬───────────────────────────┘
                              │
                              ▼
┌──────────────────── Agent Layer (smolagents) ──────────┐
│ ToolCallingAgent + LiteLLM                             │
│ - invokes tool wrappers in agent/tools.py              │
│ - tool runtime hooks emit structured telemetry         │
│ - tools use cache-before-call policy                   │
└─────────────────────┬───────────────────┬──────────────┘
                      │                   │
                      ▼                   ▼
             ┌───────────────┐   ┌──────────────────────┐
             │ PostgreSQL     │   │ epsteinexposed pkg   │
             │ - users         │   │ - remote API client   │
             │ - conversations │   │ - persons/docs/flights│
             │ - messages      │   │ - cross-search        │
             │ - api logs      │   └──────────────────────┘
             │ - tool logs     │
             │ - api call logs │
             │ - response cache│
             └───────────────┘
`;

const requestFlow = `
1) Client sends POST /api/chat with message + optional conversation_id/session_id.
2) Backend hashes IP, resolves/creates user, persists incoming message.
3) API request log row is created with status=in_progress.
4) Agent executes; each tool call:
   - computes deterministic cache key from endpoint+params
   - checks epstein_api_cache
   - on hit: returns cached payload, logs cache_hit=true
   - on miss: calls epsteinexposed, stores cache, logs cache_hit=false
5) Assistant response is persisted and streamed to client.
6) api_request_logs status finalizes to success/error.
`;

const dbModelNotes = [
  ["users", "Anonymous identities keyed by ip_hash + optional fingerprint."],
  ["conversations", "Conversation root linked to a user."],
  ["messages", "Ordered user/assistant chat messages."],
  ["api_request_logs", "Inbound API tracking (request/response/error/session)."],
  ["tool_call_logs", "Per-tool execution logs with cache flags and duration."],
  ["epstein_api_call_logs", "Downstream epsteinexposed invocation traces."],
  ["epstein_api_cache", "TTL-based response cache used before remote calls."],
];

const dosAndDonts = [
  [
    "Do",
    "Treat all person/document references as investigative context, not proof of wrongdoing.",
  ],
  [
    "Do",
    "Use `session_id` and `fingerprint` in client requests to improve telemetry continuity.",
  ],
  [
    "Do",
    "Keep tool payloads small and focused; broad prompts should be decomposed by the agent.",
  ],
  [
    "Don't",
    "Bypass service-level logging for new endpoints; observability is a non-optional requirement.",
  ],
  [
    "Don't",
    "Disable cache globally to solve one-off freshness issues; tune TTL and add explicit bypass controls instead.",
  ],
  [
    "Don't",
    "Store raw IP addresses; only hashed identifiers should be persisted.",
  ],
];

const whyAndWhatNot = [
  [
    "Why cache in DB?",
    "Repeated investigative queries are common; DB cache lowers latency and external dependency pressure.",
  ],
  [
    "What not to do",
    "Do not add in-memory-only cache as the primary store; it breaks multi-instance consistency.",
  ],
  [
    "Why SSE over polling?",
    "SSE simplifies one-way token/result streaming for chat while keeping infra footprint low.",
  ],
  [
    "What not to do",
    "Do not send giant unbounded payload previews into logs; keep previews truncated and structured.",
  ],
  [
    "Why anonymous identity?",
    "The product goal is frictionless access while preserving minimal session continuity for analytics/debugging.",
  ],
  [
    "What not to do",
    "Do not retrofit auth assumptions into core models without a migration strategy for anonymous data.",
  ],
];

const operationsRunbook = `# Start stack
cp .env.example .env
# set OPENROUTER_API_KEY
docker compose up --build

# Apply migrations only
docker compose run --rm backend alembic upgrade head

# Rebuild backend after schema/service updates
docker compose build backend
docker compose up -d backend

# Read API docs
open http://localhost:8000/docs`;

const troubleshootingRows = [
  [
    "EACCES on docs/node_modules/.vite-temp or docs/dist",
    "Container install created root-owned artifacts",
    "Run ownership fix (`chown -R <uid>:<gid> docs/node_modules docs/dist`) and rerun with Node 22.",
  ],
  [
    "Backend exits during migrations",
    "DB not reachable/resolvable at startup",
    "Use compose startup checks and verify `DATABASE_URL`, network, and `db` health.",
  ],
  [
    "High downstream API latency",
    "Cache miss ratio too high / broad queries",
    "Tune `EPSTEIN_CACHE_TTL_SECONDS`, inspect `epstein_api_call_logs`, and narrow tool queries.",
  ],
  [
    "Sparse observability data",
    "session_id/fingerprint not passed by client",
    "Ensure frontend sends `session_id` and stable fingerprint with each chat request.",
  ],
];

const securityNotes = [
  "Persist only hashed IP (`ip_hash`) and optional fingerprint; avoid raw personal identifiers.",
  "Treat `OPENROUTER_API_KEY` as secret and never commit it into repository files.",
  "Consider retention policy for logs and cache tables in production environments.",
  "Avoid exposing internal traces directly to end users without sanitization.",
];

const contributingRules = [
  "Every new endpoint must include request/response schema and persistence/telemetry behavior.",
  "Every data model change requires an Alembic migration and tests.",
  "Every caching behavior change must document key strategy and invalidation/TTL rationale.",
  "Every docs change should preserve section anchors and operational examples.",
];

function Table({
  headers,
  rows,
}: {
  headers: string[];
  rows: string[][];
}) {
  return (
    <table>
      <thead>
        <tr>
          {headers.map((h) => (
            <th key={h}>{h}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row, index) => (
          <tr key={`${row[0]}-${index}`}>
            {row.map((cell, i) => (
              <td key={`${row[0]}-${i}`}>{cell}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export function DocsApp() {
  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand">
          <p className="kicker">EpsteinExplorer</p>
          <h1>Technical Docs</h1>
        </div>
        <nav aria-label="Documentation sections">
          <ul className="toc">
            {toc.map(([id, label]) => (
              <li key={id}>
                <a href={`#${id}`}>{label}</a>
              </li>
            ))}
          </ul>
        </nav>
      </aside>

      <main className="content">
        <header className="hero" id="overview">
          <p className="eyebrow">Architecture & Operations Guide</p>
          <h2>EpsteinExplorer</h2>
          <p className="subtitle">
            Implementation-focused documentation for contributors, operators,
            and maintainers.
          </p>
        </header>

        <section className="doc-section">
          <h3>Overview</h3>
          <p>
            EpsteinExplorer is a full-stack chat research system. The frontend
            sends prompts to FastAPI via SSE. The backend orchestrates a
            smolagents tool-calling agent that queries epsteinexposed data.
            Results, telemetry, and cache state are persisted in PostgreSQL.
          </p>
          <p>
            This document focuses on implementation behavior, not product
            marketing. It is designed as an engineering reference for day-2
            operations, architecture decisions, and contribution standards.
          </p>
        </section>

        <section className="doc-section" id="conceptual-model">
          <h3>Conceptual Model</h3>
          <Table headers={["Concept", "Definition"]} rows={conceptualModelRows} />
        </section>

        <section className="doc-section" id="design-principles">
          <h3>Design Principles</h3>
          <ul>
            {designPrinciples.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>

        <section className="doc-section" id="architecture">
          <h3>Architecture</h3>
          <pre>{architectureDiagram}</pre>
        </section>

        <section className="doc-section" id="data-flow">
          <h3>Data Flow</h3>
          <pre>{requestFlow}</pre>
        </section>

        <section className="doc-section" id="persistence-model">
          <h3>Persistence Model</h3>
          <Table headers={["Table", "Purpose"]} rows={dbModelNotes} />
          <p className="hint">
            Migrations are managed through Alembic. Apply schema changes with{" "}
            <code>alembic upgrade head</code>.
          </p>
        </section>

        <section className="doc-section" id="api-reference">
          <h3>API Reference</h3>
          {endpoints.map((endpoint) => (
            <article className="endpoint" key={endpoint.path}>
              <h4>
                <span className="method">{endpoint.method}</span>{" "}
                <code>{endpoint.path}</code>
              </h4>
              <p>
                <strong>Request:</strong> <code>{endpoint.request}</code>
              </p>
              <p>
                <strong>Response:</strong> <code>{endpoint.response}</code>
              </p>
              <p>
                <strong>Notes:</strong> {endpoint.notes}
              </p>
            </article>
          ))}
        </section>

        <section className="doc-section" id="agent-tools">
          <h3>Agent Tools</h3>
          <Table headers={["Tool", "Behavior"]} rows={tools} />
        </section>

        <section className="doc-section" id="dos-donts">
          <h3>Do / Don&apos;t Guidance</h3>
          <Table headers={["Guideline", "Recommendation"]} rows={dosAndDonts} />
        </section>

        <section className="doc-section" id="why-what-not">
          <h3>Why &amp; What Not To Do</h3>
          <Table
            headers={["Decision Area", "Rationale / Anti-pattern"]}
            rows={whyAndWhatNot}
          />
        </section>

        <section className="doc-section" id="quick-start">
          <h3>Quick Start (Docker)</h3>
          <pre>{`cp .env.example .env
# set OPENROUTER_API_KEY in .env
docker compose up --build

# Frontend  : http://localhost:3000
# Backend   : http://localhost:8000
# OpenAPI   : http://localhost:8000/docs`}</pre>
          <h4>Local Development</h4>
          <pre>{`# backend
cd backend
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload

# frontend
cd frontend
npm ci
npm run dev

# docs app
cd docs
npm install
npm run dev`}</pre>
        </section>

        <section className="doc-section" id="operations">
          <h3>Operations Runbook</h3>
          <pre>{operationsRunbook}</pre>
        </section>

        <section className="doc-section" id="troubleshooting">
          <h3>Troubleshooting</h3>
          <Table
            headers={["Symptom", "Likely Cause", "Action"]}
            rows={troubleshootingRows}
          />
        </section>

        <section className="doc-section" id="configuration">
          <h3>Configuration</h3>
          <Table headers={["Variable", "Default", "Description"]} rows={envVars} />
        </section>

        <section className="doc-section" id="security">
          <h3>Security Notes</h3>
          <ul>
            {securityNotes.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>

        <section className="doc-section" id="observability">
          <h3>Caching & Observability Notes</h3>
          <ul>
            <li>
              Cache key uses deterministic hash of endpoint name + normalized
              params payload.
            </li>
            <li>
              On cache hit, tool response is returned from DB without remote API
              call.
            </li>
            <li>
              API/tool/downstream call logs are linked to user, conversation,
              session_id, and ip_hash for traceability.
            </li>
            <li>
              Large response payloads are truncated for preview fields to keep
              telemetry rows compact.
            </li>
          </ul>
        </section>

        <section className="doc-section" id="contributing">
          <h3>Contributing Standards</h3>
          <ul>
            {contributingRules.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>
      </main>
    </div>
  );
}
