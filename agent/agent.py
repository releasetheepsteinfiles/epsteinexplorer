# Credits: Erwin Lejeune — 2026-02-23
"""EpsteinAgent — importable service wrapping smolagents ToolCallingAgent."""

from __future__ import annotations

import logging
from typing import Any

from smolagents import LiteLLMModel, ToolCallingAgent

from agent.config import agent_settings
from agent.tools import ALL_TOOLS

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are EpsteinExplorer, an AI research assistant that helps users investigate "
    "the Epstein case files. You have access to tools for searching persons of interest, "
    "retrieving person details, searching documents, querying flight logs, and performing "
    "cross-type searches across documents and emails.\n\n"
    "Guidelines:\n"
    "- Be factual and measured. When data is ambiguous, say so.\n"
    "- Cite specific records (names, dates, document titles) when available.\n"
    "- Inclusion in these records does not imply guilt or wrongdoing.\n"
    "- If a query is too broad, suggest narrowing it down.\n"
    "- Use multiple tools when needed to build a comprehensive answer.\n"
    "- Format responses clearly with bullet points or tables when presenting lists."
)


class EpsteinAgent:
    """Reusable agent instance wrapping smolagents ToolCallingAgent.

    Instantiate once and call ``run(prompt)`` for each user query.
    """

    def __init__(self) -> None:
        model = LiteLLMModel(
            model_id=agent_settings.llm_model,
            api_key=agent_settings.litellm_api_key,
        )
        self._agent = ToolCallingAgent(
            tools=ALL_TOOLS,
            model=model,
            system_prompt=SYSTEM_PROMPT,
        )
        logger.info(
            "EpsteinAgent initialised with model=%s, tools=%d",
            agent_settings.llm_model,
            len(ALL_TOOLS),
        )

    def run(self, prompt: str) -> Any:
        """Run the agent on a user prompt and return the result."""
        return self._agent.run(prompt)
