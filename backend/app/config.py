# Credits: Erwin Lejeune — 2026-02-23
"""Application configuration via environment variables."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+asyncpg://explorer:explorer@localhost:5432/epsteinexplorer"
    )
    llm_model: str = "openrouter/google/gemini-2.0-flash-001"
    openrouter_api_key: str = ""
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    epstein_cache_ttl_seconds: int = 3600
    observability_preview_chars: int = 2000

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
