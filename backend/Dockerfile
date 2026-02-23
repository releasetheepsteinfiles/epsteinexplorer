# Credits: Erwin Lejeune — 2026-02-23
FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY backend/pyproject.toml .
RUN uv pip install --system -e "."

COPY backend/app/ app/
COPY agent/ agent/
COPY backend/alembic.ini .
COPY backend/alembic/ alembic/

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
