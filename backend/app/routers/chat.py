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

from app.database import get_db
from app.models.conversation import Conversation, Message
from app.schemas import ChatRequest
from app.services.user_service import hash_ip, resolve_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


def _get_agent():
    from agent import EpsteinAgent

    return EpsteinAgent()


@router.post("/chat")
async def chat(
    body: ChatRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Run the agent on user input and stream the response via SSE."""
    ip_h = hash_ip(request)
    user = await resolve_user(db, ip_h, body.fingerprint)

    if body.conversation_id:
        conv_id = uuid.UUID(body.conversation_id)
    else:
        conv = Conversation(user_id=user.id)
        db.add(conv)
        await db.flush()
        conv_id = conv.id

    db.add(Message(conversation_id=conv_id, role="user", content=body.message))
    await db.commit()

    async def _stream() -> AsyncGenerator[str, None]:
        try:
            agent = _get_agent()
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, partial(agent.run, body.message))
            content = str(result)

            async with async_session_ctx() as sdb:
                sdb.add(
                    Message(conversation_id=conv_id, role="assistant", content=content)
                )
                await sdb.commit()

            yield json.dumps({"type": "message", "content": content})
        except Exception as exc:
            logger.exception("Agent error")
            yield json.dumps({"type": "error", "content": str(exc)})

        yield json.dumps({"type": "done", "conversation_id": str(conv_id)})

    from app.database import async_session as async_session_ctx

    return EventSourceResponse(_stream())
