# Credits: Erwin Lejeune — 2026-02-23
"""Smolagents @tool wrappers around the epsteinexposed client.

Each tool uses the synchronous EpsteinExposed client because smolagents
tool functions are called synchronously by the agent.
"""

from __future__ import annotations

import contextvars
import json
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Protocol

from smolagents import tool

from epsteinexposed import EpsteinExposed


class RuntimeHooks(Protocol):
    def cache_get(
        self, endpoint: str, params_payload: dict[str, Any]
    ) -> str | None: ...
    def cache_set(
        self, endpoint: str, params_payload: dict[str, Any], response_payload: str
    ) -> str: ...
    def log_tool_call(self, event: dict[str, Any]) -> None: ...
    def log_api_call(self, event: dict[str, Any]) -> None: ...


@dataclass
class _NoopHooks:
    def cache_get(self, endpoint: str, params_payload: dict[str, Any]) -> str | None:
        return None

    def cache_set(
        self, endpoint: str, params_payload: dict[str, Any], response_payload: str
    ) -> str:
        return ""

    def log_tool_call(self, event: dict[str, Any]) -> None:
        return None

    def log_api_call(self, event: dict[str, Any]) -> None:
        return None


_RUNTIME_HOOKS: contextvars.ContextVar[RuntimeHooks] = contextvars.ContextVar(
    "runtime_hooks", default=_NoopHooks()
)


@contextmanager
def runtime_hooks_context(hooks: RuntimeHooks | None):
    token = _RUNTIME_HOOKS.set(hooks or _NoopHooks())
    try:
        yield
    finally:
        _RUNTIME_HOOKS.reset(token)


def _client() -> EpsteinExposed:
    return EpsteinExposed()


def _recorded_call(
    *,
    tool_name: str,
    endpoint: str,
    params_payload: dict[str, Any],
    call_and_transform,
) -> str:
    hooks = _RUNTIME_HOOKS.get()
    started = time.perf_counter()
    cache_hit = False

    try:
        cached = hooks.cache_get(endpoint, params_payload)
        if cached:
            cache_hit = True
            payload = cached
            hooks.log_api_call(
                {
                    "endpoint": endpoint,
                    "params_payload": params_payload,
                    "cache_hit": True,
                    "cache_key": "",
                    "response_preview": payload[:1000],
                    "success": True,
                    "duration_ms": (time.perf_counter() - started) * 1000,
                }
            )
        else:
            payload = call_and_transform()
            cache_key = hooks.cache_set(endpoint, params_payload, payload)
            hooks.log_api_call(
                {
                    "endpoint": endpoint,
                    "params_payload": params_payload,
                    "cache_hit": False,
                    "cache_key": cache_key,
                    "response_preview": payload[:1000],
                    "success": True,
                    "duration_ms": (time.perf_counter() - started) * 1000,
                }
            )

        hooks.log_tool_call(
            {
                "tool_name": tool_name,
                "input_payload": params_payload,
                "output_preview": payload[:1000],
                "cache_hit": cache_hit,
                "success": True,
                "duration_ms": (time.perf_counter() - started) * 1000,
            }
        )
        return payload
    except Exception as exc:
        hooks.log_tool_call(
            {
                "tool_name": tool_name,
                "input_payload": params_payload,
                "cache_hit": cache_hit,
                "success": False,
                "error": str(exc),
                "duration_ms": (time.perf_counter() - started) * 1000,
            }
        )
        hooks.log_api_call(
            {
                "endpoint": endpoint,
                "params_payload": params_payload,
                "cache_hit": cache_hit,
                "success": False,
                "error": str(exc),
                "duration_ms": (time.perf_counter() - started) * 1000,
            }
        )
        raise


@tool
def search_persons(name: str, category: str = "") -> str:
    """Search the Epstein files for persons of interest by name or category.

    Args:
        name: Full or partial person name to search for.
        category: Optional category filter (politician, business, royalty, celebrity,
                  associate, legal, academic, socialite, military-intelligence, other).

    Returns:
        JSON with matching persons including stats (flights, documents, etc.).
    """
    params_payload = {"name": name, "category": category}
    return _recorded_call(
        tool_name="search_persons",
        endpoint="search_persons",
        params_payload=params_payload,
        call_and_transform=lambda: _search_persons_uncached(name, category),
    )


def _search_persons_uncached(name: str, category: str) -> str:
    with _client() as client:
        result = client.search_persons(
            q=name or None, category=category or None, per_page=20
        )
    return json.dumps(
        {
            "total": result.meta.total,
            "persons": [
                {
                    "name": p.name,
                    "slug": p.slug,
                    "category": p.category,
                    "short_bio": p.short_bio,
                    "stats": p.stats.model_dump() if p.stats else {},
                }
                for p in result.data
            ],
        },
        indent=2,
    )


@tool
def get_person_detail(slug: str) -> str:
    """Get full detail for a specific person by their URL slug.

    Returns biographical info, aliases, black book entry status, and aggregate stats.

    Args:
        slug: The person's URL slug (e.g. "bill-clinton", "ghislaine-maxwell").

    Returns:
        JSON with full person detail.
    """
    params_payload = {"slug": slug}
    return _recorded_call(
        tool_name="get_person_detail",
        endpoint="get_person_detail",
        params_payload=params_payload,
        call_and_transform=lambda: _get_person_detail_uncached(slug),
    )


def _get_person_detail_uncached(slug: str) -> str:
    with _client() as client:
        p = client.get_person(slug)
    return json.dumps(
        {
            "name": p.name,
            "slug": p.slug,
            "category": p.category,
            "bio": p.bio,
            "aliases": p.aliases,
            "black_book_entry": p.black_book_entry,
            "stats": p.stats.model_dump() if p.stats else {},
        },
        indent=2,
    )


@tool
def search_documents(query: str, source: str = "") -> str:
    """Search Epstein case documents using full-text search.

    Args:
        query: Full-text search query (e.g. "little st james", "flight log").
        source: Optional source filter (court-filing, doj-release, fbi, efta).

    Returns:
        JSON with matching documents including title, date, source, summary.
    """
    params_payload = {"query": query, "source": source}
    return _recorded_call(
        tool_name="search_documents",
        endpoint="search_documents",
        params_payload=params_payload,
        call_and_transform=lambda: _search_documents_uncached(query, source),
    )


def _search_documents_uncached(query: str, source: str) -> str:
    with _client() as client:
        result = client.search_documents(
            q=query or None, source=source or None, per_page=20
        )
    return json.dumps(
        {
            "total": result.meta.total,
            "documents": [
                {
                    "id": d.id,
                    "title": d.title,
                    "date": d.date,
                    "source": d.source,
                    "summary": d.summary,
                    "tags": d.tags,
                }
                for d in result.data
            ],
        },
        indent=2,
    )


@tool
def search_flights(
    passenger: str = "", year: str = "", origin: str = "", destination: str = ""
) -> str:
    """Search Epstein's flight logs (~1997-2006) across all known aircraft.

    Args:
        passenger: Filter by passenger name.
        year: Filter by year (e.g. "2002").
        origin: Filter by departure location.
        destination: Filter by arrival location.

    Returns:
        JSON with flight records including date, route, and passengers.
    """
    params_payload = {
        "passenger": passenger,
        "year": year,
        "origin": origin,
        "destination": destination,
    }
    return _recorded_call(
        tool_name="search_flights",
        endpoint="search_flights",
        params_payload=params_payload,
        call_and_transform=lambda: _search_flights_uncached(
            passenger, year, origin, destination
        ),
    )


def _search_flights_uncached(
    passenger: str, year: str, origin: str, destination: str
) -> str:
    year_int = int(year) if year else None
    with _client() as client:
        result = client.search_flights(
            passenger=passenger or None,
            year=year_int,
            origin=origin or None,
            destination=destination or None,
            per_page=20,
        )
    return json.dumps(
        {
            "total": result.meta.total,
            "flights": [
                {
                    "id": f.id,
                    "date": f.date,
                    "origin": f.origin,
                    "destination": f.destination,
                    "passenger_names": f.passenger_names,
                    "passenger_count": f.passenger_count,
                }
                for f in result.data
            ],
        },
        indent=2,
    )


@tool
def cross_search(query: str, type: str = "") -> str:
    """Search across documents AND emails simultaneously.

    Args:
        query: Search query (required).
        type: Limit to "documents" or "emails". Leave empty to search both.

    Returns:
        JSON with separate result arrays for documents and emails.
    """
    params_payload = {"query": query, "type": type}
    return _recorded_call(
        tool_name="cross_search",
        endpoint="cross_search",
        params_payload=params_payload,
        call_and_transform=lambda: _cross_search_uncached(query, type),
    )


def _cross_search_uncached(query: str, type: str) -> str:
    with _client() as client:
        result = client.search(q=query, type=type or None, limit=20)
    return json.dumps(
        {
            "documents": result.documents.results,
            "emails": result.emails.results,
        },
        indent=2,
    )


ALL_TOOLS = [
    search_persons,
    get_person_detail,
    search_documents,
    search_flights,
    cross_search,
]
