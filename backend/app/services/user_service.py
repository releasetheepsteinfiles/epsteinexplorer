# Credits: Erwin Lejeune — 2026-02-23
"""Anonymous user resolution from IP hash + fingerprint."""

from __future__ import annotations

import hashlib

from fastapi import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


def hash_ip(request: Request) -> str:
    """SHA-256 hash of the client IP address."""
    forwarded = request.headers.get("x-forwarded-for")
    ip = (
        forwarded.split(",")[0].strip()
        if forwarded
        else (request.client.host if request.client else "unknown")
    )
    return hashlib.sha256(ip.encode()).hexdigest()


async def resolve_user(
    db: AsyncSession, ip_hash: str, fingerprint: str | None = None
) -> User:
    """Find or create an anonymous user by IP hash + fingerprint."""
    stmt = select(User).where(User.ip_hash == ip_hash)
    if fingerprint:
        stmt = stmt.where(User.fingerprint == fingerprint)

    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        user = User(ip_hash=ip_hash, fingerprint=fingerprint)
        db.add(user)
        await db.flush()

    return user
