# Credits: Erwin Lejeune — 2026-02-23
"""Tests for the chat endpoint."""

from __future__ import annotations

import pytest
from sqlalchemy import select

from app.models.user import User
from app.services.user_service import resolve_user


@pytest.mark.asyncio
async def test_resolve_user_creates_new(db):
    user = await resolve_user(db, ip_hash="d" * 64, fingerprint="fp1")
    await db.commit()

    result = await db.execute(select(User).where(User.ip_hash == "d" * 64))
    found = result.scalar_one()
    assert found.id == user.id
    assert found.fingerprint == "fp1"


@pytest.mark.asyncio
async def test_resolve_user_returns_existing(db):
    user1 = await resolve_user(db, ip_hash="e" * 64)
    await db.commit()

    user2 = await resolve_user(db, ip_hash="e" * 64)
    assert user2.id == user1.id


@pytest.mark.asyncio
async def test_resolve_user_differentiates_fingerprint(db):
    user1 = await resolve_user(db, ip_hash="f" * 64, fingerprint="fp_a")
    await db.commit()

    user2 = await resolve_user(db, ip_hash="f" * 64, fingerprint="fp_b")
    await db.commit()

    assert user1.id != user2.id
