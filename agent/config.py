# Credits: Erwin Lejeune — 2026-02-23
"""Agent configuration."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class AgentSettings(BaseSettings):
    llm_model: str = "gemini/gemini-2.0-flash"
    litellm_api_key: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


agent_settings = AgentSettings()
