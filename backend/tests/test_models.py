# Credits: Erwin Lejeune — 2026-02-23
"""Tests for database models."""

from __future__ import annotations

import pytest
from sqlalchemy import select

from app.models.conversation import Conversation, Message
from app.models.user import User


@pytest.mark.asyncio
async def test_create_user(db):
    user = User(ip_hash="a" * 64)
    db.add(user)
    await db.flush()

    result = await db.execute(select(User).where(User.ip_hash == "a" * 64))
    found = result.scalar_one()
    assert found.id == user.id
    assert found.fingerprint is None


@pytest.mark.asyncio
async def test_create_user_with_fingerprint(db):
    user = User(ip_hash="b" * 64, fingerprint="fp123")
    db.add(user)
    await db.flush()

    result = await db.execute(select(User))
    found = result.scalar_one()
    assert found.fingerprint == "fp123"


@pytest.mark.asyncio
async def test_conversation_and_messages(db):
    user = User(ip_hash="c" * 64)
    db.add(user)
    await db.flush()

    conv = Conversation(user_id=user.id)
    db.add(conv)
    await db.flush()

    db.add(Message(conversation_id=conv.id, role="user", content="Hello"))
    db.add(Message(conversation_id=conv.id, role="assistant", content="Hi there"))
    await db.flush()

    result = await db.execute(select(Message).where(Message.conversation_id == conv.id))
    messages = result.scalars().all()
    assert len(messages) == 2
    assert messages[0].role == "user"
    assert messages[1].role == "assistant"
