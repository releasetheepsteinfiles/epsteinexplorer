# Credits: Erwin Lejeune — 2026-02-23
"""Tests for agent tools — mock the epsteinexposed client."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from epsteinexposed.models import (
    Document,
    Flight,
    PaginatedResponse,
    PaginationMeta,
    Person,
    PersonDetail,
    PersonStats,
    SearchResults,
)

from agent.tools import (
    cross_search,
    get_person_detail,
    search_documents,
    search_flights,
    search_persons,
)


def _paginated(data, model_cls, total=None):
    return PaginatedResponse[model_cls](
        status="ok",
        data=data,
        meta=PaginationMeta(total=total or len(data)),
    )


class TestSearchPersons:
    @patch("agent.tools._client")
    def test_returns_persons(self, mock_factory):
        mock_client = MagicMock()
        mock_factory.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_factory.return_value.__exit__ = MagicMock(return_value=False)
        mock_client.search_persons.return_value = _paginated(
            [
                Person(
                    id=1,
                    name="Test Person",
                    slug="test-person",
                    stats=PersonStats(flights=5),
                )
            ],
            Person,
        )
        result = json.loads(search_persons("test"))
        assert result["total"] == 1
        assert result["persons"][0]["name"] == "Test Person"
        assert result["persons"][0]["stats"]["flights"] == 5


class TestGetPersonDetail:
    @patch("agent.tools._client")
    def test_returns_detail(self, mock_factory):
        mock_client = MagicMock()
        mock_factory.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_factory.return_value.__exit__ = MagicMock(return_value=False)
        mock_client.get_person.return_value = PersonDetail(
            id=1,
            name="Jane Doe",
            slug="jane-doe",
            bio="Bio text",
            aliases=["J. Doe"],
            black_book_entry=True,
            stats=PersonStats(flights=10, documents=3),
        )
        result = json.loads(get_person_detail("jane-doe"))
        assert result["name"] == "Jane Doe"
        assert result["black_book_entry"] is True
        assert result["aliases"] == ["J. Doe"]


class TestSearchDocuments:
    @patch("agent.tools._client")
    def test_returns_documents(self, mock_factory):
        mock_client = MagicMock()
        mock_factory.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_factory.return_value.__exit__ = MagicMock(return_value=False)
        mock_client.search_documents.return_value = _paginated(
            [Document(id="d1", title="Deposition", source="court-filing")],
            Document,
        )
        result = json.loads(search_documents("deposition"))
        assert result["total"] == 1
        assert result["documents"][0]["title"] == "Deposition"


class TestSearchFlights:
    @patch("agent.tools._client")
    def test_returns_flights(self, mock_factory):
        mock_client = MagicMock()
        mock_factory.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_factory.return_value.__exit__ = MagicMock(return_value=False)
        mock_client.search_flights.return_value = _paginated(
            [
                Flight(
                    id=1,
                    date="2002-01-15",
                    origin="Palm Beach",
                    destination="Teterboro",
                    passenger_names=["A"],
                    passenger_count=1,
                )
            ],
            Flight,
        )
        result = json.loads(search_flights(passenger="A"))
        assert result["flights"][0]["origin"] == "Palm Beach"


class TestCrossSearch:
    @patch("agent.tools._client")
    def test_returns_results(self, mock_factory):
        mock_client = MagicMock()
        mock_factory.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_factory.return_value.__exit__ = MagicMock(return_value=False)
        mock_client.search.return_value = SearchResults(
            status="ok",
            documents={"results": [{"id": "d1", "title": "T"}]},
            emails={"results": []},
        )
        result = json.loads(cross_search("wexner"))
        assert len(result["documents"]) == 1
        assert result["emails"] == []
