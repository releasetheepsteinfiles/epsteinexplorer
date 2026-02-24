# Credits: Erwin Lejeune — 2026-02-24
"""DB-backed observability and caching services."""

from __future__ import annotations

import hashlib
import json
import uuid
from collections.abc import Iterable
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.observability import (
    ApiRequestLog,
    EpsteinApiCache,
    EpsteinApiCallLog,
    ToolCallLog,
)


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)


def build_cache_key(endpoint: str, params_payload: dict[str, Any]) -> str:
    seed = f"{endpoint}:{canonical_json(params_payload)}".encode("utf-8")
    return hashlib.sha256(seed).hexdigest()


def preview_text(content: str | None) -> str | None:
    if content is None:
        return None
    if len(content) <= settings.observability_preview_chars:
        return content
    return content[: settings.observability_preview_chars]


async def get_cached_response(
    db: AsyncSession, endpoint: str, params_payload: dict[str, Any]
) -> str | None:
    cache_key = build_cache_key(endpoint, params_payload)
    now = datetime.now(UTC)
    result = await db.execute(
        select(EpsteinApiCache).where(
            and_(
                EpsteinApiCache.cache_key == cache_key,
                or_(
                    EpsteinApiCache.expires_at.is_(None),
                    EpsteinApiCache.expires_at > now,
                ),
            )
        )
    )
    row = result.scalar_one_or_none()
    if row is None:
        return None
    row.hit_count = int(row.hit_count or 0) + 1
    await db.flush()
    return row.response_payload


async def upsert_cached_response(
    db: AsyncSession,
    endpoint: str,
    params_payload: dict[str, Any],
    response_payload: str,
) -> str:
    cache_key = build_cache_key(endpoint, params_payload)
    result = await db.execute(
        select(EpsteinApiCache).where(EpsteinApiCache.cache_key == cache_key)
    )
    row = result.scalar_one_or_none()
    expires_at = datetime.now(UTC) + timedelta(
        seconds=settings.epstein_cache_ttl_seconds
    )

    if row is None:
        row = EpsteinApiCache(
            endpoint=endpoint,
            params_payload=params_payload,
            cache_key=cache_key,
            response_payload=response_payload,
            hit_count=0,
            expires_at=expires_at,
        )
        db.add(row)
    else:
        row.endpoint = endpoint
        row.params_payload = params_payload
        row.response_payload = response_payload
        row.expires_at = expires_at
    await db.flush()
    return cache_key


async def create_api_request_log(
    db: AsyncSession,
    *,
    user_id: uuid.UUID,
    conversation_id: uuid.UUID,
    session_id: str | None,
    ip_hash: str,
    fingerprint: str | None,
    method: str,
    path: str,
    request_body: dict[str, Any],
) -> ApiRequestLog:
    row = ApiRequestLog(
        user_id=user_id,
        conversation_id=conversation_id,
        session_id=session_id,
        ip_hash=ip_hash,
        fingerprint=fingerprint,
        method=method,
        path=path,
        request_body=request_body,
        status="in_progress",
    )
    db.add(row)
    await db.flush()
    return row


async def finalize_api_request_log(
    db: AsyncSession,
    request_log_id: uuid.UUID,
    *,
    status: str,
    response_body: str | None = None,
    error: str | None = None,
) -> None:
    row = await db.get(ApiRequestLog, request_log_id)
    if row is None:
        return
    row.status = status
    row.response_body = preview_text(response_body)
    row.error = preview_text(error)
    row.completed_at = datetime.now(UTC)
    await db.flush()


async def persist_tool_call_logs(
    db: AsyncSession,
    *,
    events: Iterable[dict[str, Any]],
    user_id: uuid.UUID,
    conversation_id: uuid.UUID,
    api_request_log_id: uuid.UUID,
    session_id: str | None,
    ip_hash: str,
) -> list[uuid.UUID]:
    ids: list[uuid.UUID] = []
    for e in events:
        row = ToolCallLog(
            user_id=user_id,
            conversation_id=conversation_id,
            api_request_log_id=api_request_log_id,
            session_id=session_id,
            ip_hash=ip_hash,
            tool_name=e.get("tool_name", "unknown"),
            input_payload=e.get("input_payload", {}),
            output_preview=preview_text(e.get("output_preview")),
            cache_hit=bool(e.get("cache_hit", False)),
            success=bool(e.get("success", True)),
            error=preview_text(e.get("error")),
            duration_ms=float(e["duration_ms"])
            if e.get("duration_ms") is not None
            else None,
        )
        db.add(row)
        await db.flush()
        ids.append(row.id)
    return ids


async def persist_epstein_api_call_logs(
    db: AsyncSession,
    *,
    events: Iterable[dict[str, Any]],
    user_id: uuid.UUID,
    conversation_id: uuid.UUID,
    api_request_log_id: uuid.UUID,
    session_id: str | None,
    ip_hash: str,
) -> None:
    for e in events:
        row = EpsteinApiCallLog(
            user_id=user_id,
            conversation_id=conversation_id,
            tool_call_log_id=e.get("tool_call_log_id"),
            api_request_log_id=api_request_log_id,
            session_id=session_id,
            ip_hash=ip_hash,
            endpoint=e.get("endpoint", "unknown"),
            params_payload=e.get("params_payload", {}),
            cache_key=e.get("cache_key", ""),
            cache_hit=bool(e.get("cache_hit", False)),
            response_preview=preview_text(e.get("response_preview")),
            success=bool(e.get("success", True)),
            error=preview_text(e.get("error")),
            duration_ms=float(e["duration_ms"])
            if e.get("duration_ms") is not None
            else None,
        )
        db.add(row)
    await db.flush()
