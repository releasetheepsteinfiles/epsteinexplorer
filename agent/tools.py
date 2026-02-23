# Credits: Erwin Lejeune — 2026-02-23
"""Smolagents @tool wrappers around the epsteinexposed client.

Each tool uses the synchronous EpsteinExposed client because smolagents
tool functions are called synchronously by the agent.
"""

from __future__ import annotations

import json

from smolagents import tool

from epsteinexposed import EpsteinExposed


def _client() -> EpsteinExposed:
    return EpsteinExposed()


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
