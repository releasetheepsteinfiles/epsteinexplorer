# Credits: Erwin Lejeune — 2026-02-23
"""Application configuration via environment variables."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+asyncpg://explorer:explorer@localhost:5432/epsteinexplorer"
    )
    llm_model: str = "gemini/gemini-2.0-flash"
    litellm_api_key: str = ""
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
