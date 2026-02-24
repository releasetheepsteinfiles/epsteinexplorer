// Credits: Erwin Lejeune — 2026-02-24
const quickStart = [
  "cp .env.example .env",
  "Edit .env and set OPENROUTER_API_KEY",
  "docker compose up --build",
];

const apiEndpoints = [
  { method: "GET", path: "/api/health", purpose: "Backend health check" },
  { method: "POST", path: "/api/chat", purpose: "SSE chat with the agent" },
  { method: "GET", path: "/docs", purpose: "FastAPI OpenAPI UI" },
];

const tools = [
  "search_persons",
  "get_person_detail",
  "search_documents",
  "search_flights",
  "cross_search",
];

export function DocsApp() {
  return (
    <div className="page">
      <header className="hero">
        <p className="kicker">EpsteinExplorer</p>
        <h1>Documentation</h1>
        <p className="subtitle">
          A modern docs web app powered by Vite + React.
        </p>
      </header>

      <main className="grid">
        <section className="card">
          <h2>Architecture</h2>
          <p>
            Frontend chat UI sends prompts to FastAPI over SSE. Backend calls a
            smolagents tool-calling agent with epsteinexposed-powered tools,
            then persists conversations, request logs, tool calls, and cache in
            PostgreSQL.
          </p>
        </section>

        <section className="card">
          <h2>Quick Start</h2>
          <ol>
            {quickStart.map((step) => (
              <li key={step}>
                <code>{step}</code>
              </li>
            ))}
          </ol>
          <p className="hint">
            Frontend: <code>http://localhost:3000</code> | Backend:{" "}
            <code>http://localhost:8000</code>
          </p>
        </section>

        <section className="card">
          <h2>API</h2>
          <ul>
            {apiEndpoints.map((endpoint) => (
              <li key={endpoint.path}>
                <strong>{endpoint.method}</strong> <code>{endpoint.path}</code>{" "}
                - {endpoint.purpose}
              </li>
            ))}
          </ul>
        </section>

        <section className="card">
          <h2>Agent Tools</h2>
          <ul>
            {tools.map((tool) => (
              <li key={tool}>
                <code>{tool}</code>
              </li>
            ))}
          </ul>
        </section>
      </main>
    </div>
  );
}
