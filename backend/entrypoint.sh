#!/usr/bin/env sh
# Credits: Erwin Lejeune — 2026-02-24

set -eu

echo "Waiting for database connectivity..."
python - <<'PY'
import os
import socket
import time
from urllib.parse import urlparse

db_url = os.getenv("DATABASE_URL", "")
if not db_url:
    raise SystemExit("DATABASE_URL is not set")

parsed = urlparse(db_url)
host = parsed.hostname
port = parsed.port or 5432

if not host:
    raise SystemExit(f"Could not parse DB host from DATABASE_URL: {db_url!r}")

deadline = time.time() + 60
last_error = None
while time.time() < deadline:
    try:
        socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
        s = socket.create_connection((host, port), timeout=2)
        s.close()
        print(f"Database reachable at {host}:{port}")
        raise SystemExit(0)
    except OSError as exc:
        last_error = exc
        time.sleep(2)

raise SystemExit(f"Database not reachable at {host}:{port} after 60s: {last_error}")
PY

echo "Running migrations..."
alembic upgrade head

echo "Starting API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
