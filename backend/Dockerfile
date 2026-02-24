# Credits: Erwin Lejeune — 2026-02-23
FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY backend/pyproject.toml .
COPY backend/app/ app/
COPY agent/ agent/
COPY backend/alembic.ini .
COPY backend/alembic/ alembic/
COPY backend/entrypoint.sh /entrypoint.sh

RUN uv pip install --system .
RUN chmod +x /entrypoint.sh

EXPOSE 8000

CMD ["/entrypoint.sh"]
