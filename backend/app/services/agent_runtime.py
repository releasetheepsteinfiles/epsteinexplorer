# Credits: Erwin Lejeune — 2026-02-24
"""Thread-safe runtime hooks used by the agent tools."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Any


class AgentRuntimeHooks:
    """Bridge sync tool execution (threadpool) with async DB cache operations."""

    def __init__(
        self,
        *,
        loop: asyncio.AbstractEventLoop,
        cache_get_async: Callable[[str, dict[str, Any]], Any],
        cache_set_async: Callable[[str, dict[str, Any], str], Any],
    ) -> None:
        self._loop = loop
        self._cache_get_async = cache_get_async
        self._cache_set_async = cache_set_async
        self.tool_events: list[dict[str, Any]] = []
        self.api_events: list[dict[str, Any]] = []

    def cache_get(self, endpoint: str, params_payload: dict[str, Any]) -> str | None:
        fut = asyncio.run_coroutine_threadsafe(
            self._cache_get_async(endpoint, params_payload), self._loop
        )
        return fut.result(timeout=20)

    def cache_set(
        self, endpoint: str, params_payload: dict[str, Any], response_payload: str
    ) -> str:
        fut = asyncio.run_coroutine_threadsafe(
            self._cache_set_async(endpoint, params_payload, response_payload),
            self._loop,
        )
        return fut.result(timeout=20)

    def log_tool_call(self, event: dict[str, Any]) -> None:
        self.tool_events.append(event)

    def log_api_call(self, event: dict[str, Any]) -> None:
        self.api_events.append(event)
