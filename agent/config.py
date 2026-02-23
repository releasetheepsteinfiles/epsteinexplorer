# Credits: Erwin Lejeune — 2026-02-23
"""Agent configuration."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class AgentSettings(BaseSettings):
    llm_model: str = "gpt-4o-mini"
    litellm_api_key: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


agent_settings = AgentSettings()
