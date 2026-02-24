# Credits: Erwin Lejeune — 2026-02-24
"""Tests for observability persistence and epsteinexposed cache."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import select

from app.models.conversation import Conversation
from app.models.observability import (
    ApiRequestLog,
    EpsteinApiCallLog,
    EpsteinApiCache,
    ToolCallLog,
)
from app.models.user import User
from app.services.observability_service import (
    create_api_request_log,
    get_cached_response,
    persist_epstein_api_call_logs,
    persist_tool_call_logs,
    upsert_cached_response,
)


@pytest.mark.asyncio
async def test_epstein_cache_roundtrip(db):
    endpoint = "search_persons"
    params = {"name": "Doe", "category": ""}
    payload = '{"total": 1, "persons": []}'

    key = await upsert_cached_response(db, endpoint, params, payload)
    await db.commit()

    cached = await get_cached_response(db, endpoint, params)
    await db.commit()
    assert cached == payload

    row = (await db.execute(select(EpsteinApiCache))).scalar_one()
    assert row.cache_key == key
    assert row.hit_count == 1


@pytest.mark.asyncio
async def test_observability_logs_are_persisted(db):
    user = User(ip_hash="9" * 64, fingerprint="fp-x")
    db.add(user)
    await db.flush()
    conv = Conversation(user_id=user.id)
    db.add(conv)
    await db.flush()

    req = await create_api_request_log(
        db,
        user_id=user.id,
        conversation_id=conv.id,
        session_id="sess-1",
        ip_hash=user.ip_hash,
        fingerprint=user.fingerprint,
        method="POST",
        path="/api/chat",
        request_body={"message": "hello"},
    )
    await persist_tool_call_logs(
        db,
        events=[
            {
                "tool_name": "search_persons",
                "input_payload": {"name": "Doe"},
                "output_preview": "{}",
                "cache_hit": True,
                "success": True,
                "duration_ms": 2.5,
            }
        ],
        user_id=user.id,
        conversation_id=conv.id,
        api_request_log_id=req.id,
        session_id="sess-1",
        ip_hash=user.ip_hash,
    )
    await persist_epstein_api_call_logs(
        db,
        events=[
            {
                "endpoint": "search_persons",
                "params_payload": {"name": "Doe"},
                "cache_key": "abc",
                "cache_hit": True,
                "response_preview": "{}",
                "success": True,
                "duration_ms": 1.2,
                "tool_call_log_id": uuid.uuid4(),
            }
        ],
        user_id=user.id,
        conversation_id=conv.id,
        api_request_log_id=req.id,
        session_id="sess-1",
        ip_hash=user.ip_hash,
    )
    await db.commit()

    assert (await db.execute(select(ApiRequestLog))).scalar_one().path == "/api/chat"
    assert (
        await db.execute(select(ToolCallLog))
    ).scalar_one().tool_name == "search_persons"
    assert (
        await db.execute(select(EpsteinApiCallLog))
    ).scalar_one().endpoint == "search_persons"
