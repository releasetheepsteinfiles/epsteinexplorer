# Credits: Erwin Lejeune — 2026-02-23
"""Pydantic request/response schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: str | None = None
    fingerprint: str | None = None
    session_id: str | None = Field(default=None, max_length=128)


class ChatEvent(BaseModel):
    type: str
    content: str = ""


class MessageOut(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationOut(BaseModel):
    id: str
    created_at: datetime
    messages: list[MessageOut] = []

    model_config = {"from_attributes": True}
