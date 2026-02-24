# Credits: Erwin Lejeune — 2026-02-23
"""Chat endpoint — streams agent responses via SSE."""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from collections.abc import AsyncGenerator
from functools import partial

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from app.database import async_session as async_session_ctx
from app.database import get_db
from app.models.conversation import Conversation, Message
from app.schemas import ChatRequest
from app.services.agent_runtime import AgentRuntimeHooks
from app.services.observability_service import (
    create_api_request_log,
    finalize_api_request_log,
    get_cached_response,
    persist_epstein_api_call_logs,
    persist_tool_call_logs,
    upsert_cached_response,
)
from app.services.user_service import hash_ip, resolve_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


def _get_agent(runtime_hooks=None):
    from agent import EpsteinAgent

    return EpsteinAgent(runtime_hooks=runtime_hooks)


@router.post("/chat")
async def chat(
    body: ChatRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Run the agent on user input and stream the response via SSE."""
    ip_h = hash_ip(request)
    user = await resolve_user(db, ip_h, body.fingerprint)
    session_id = body.session_id or request.headers.get("x-session-id")

    if body.conversation_id:
        conv_id = uuid.UUID(body.conversation_id)
    else:
        conv = Conversation(user_id=user.id)
        db.add(conv)
        await db.flush()
        conv_id = conv.id

    db.add(Message(conversation_id=conv_id, role="user", content=body.message))
    request_log = await create_api_request_log(
        db,
        user_id=user.id,
        conversation_id=conv_id,
        session_id=session_id,
        ip_hash=ip_h,
        fingerprint=body.fingerprint,
        method=request.method,
        path=str(request.url.path),
        request_body={
            "message": body.message,
            "conversation_id": str(conv_id),
            "fingerprint": body.fingerprint,
            "session_id": session_id,
        },
    )
    await db.commit()

    loop = asyncio.get_running_loop()

    async def _cache_get(endpoint: str, params_payload: dict) -> str | None:
        async with async_session_ctx() as sdb:
            payload = await get_cached_response(sdb, endpoint, params_payload)
            await sdb.commit()
            return payload

    async def _cache_set(endpoint: str, params_payload: dict, payload: str) -> str:
        async with async_session_ctx() as sdb:
            cache_key = await upsert_cached_response(
                sdb, endpoint, params_payload, payload
            )
            await sdb.commit()
            return cache_key

    runtime_hooks = AgentRuntimeHooks(
        loop=loop,
        cache_get_async=_cache_get,
        cache_set_async=_cache_set,
    )

    async def _stream() -> AsyncGenerator[str, None]:
        try:
            agent = _get_agent(runtime_hooks=runtime_hooks)
            result = await loop.run_in_executor(None, partial(agent.run, body.message))
            content = str(result)

            async with async_session_ctx() as sdb:
                sdb.add(
                    Message(conversation_id=conv_id, role="assistant", content=content)
                )
                await persist_tool_call_logs(
                    sdb,
                    events=runtime_hooks.tool_events,
                    user_id=user.id,
                    conversation_id=conv_id,
                    api_request_log_id=request_log.id,
                    session_id=session_id,
                    ip_hash=ip_h,
                )
                await persist_epstein_api_call_logs(
                    sdb,
                    events=runtime_hooks.api_events,
                    user_id=user.id,
                    conversation_id=conv_id,
                    api_request_log_id=request_log.id,
                    session_id=session_id,
                    ip_hash=ip_h,
                )
                await finalize_api_request_log(
                    sdb, request_log.id, status="success", response_body=content
                )
                await sdb.commit()

            yield json.dumps({"type": "message", "content": content})
        except Exception as exc:
            logger.exception("Agent error")
            async with async_session_ctx() as sdb:
                await persist_tool_call_logs(
                    sdb,
                    events=runtime_hooks.tool_events,
                    user_id=user.id,
                    conversation_id=conv_id,
                    api_request_log_id=request_log.id,
                    session_id=session_id,
                    ip_hash=ip_h,
                )
                await persist_epstein_api_call_logs(
                    sdb,
                    events=runtime_hooks.api_events,
                    user_id=user.id,
                    conversation_id=conv_id,
                    api_request_log_id=request_log.id,
                    session_id=session_id,
                    ip_hash=ip_h,
                )
                await finalize_api_request_log(
                    sdb, request_log.id, status="error", error=str(exc)
                )
                await sdb.commit()
            yield json.dumps({"type": "error", "content": str(exc)})

        yield json.dumps({"type": "done", "conversation_id": str(conv_id)})

    return EventSourceResponse(_stream())
