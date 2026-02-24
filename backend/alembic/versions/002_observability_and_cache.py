# Credits: Erwin Lejeune — 2026-02-24
"""Add observability and cache tables.

Revision ID: 002
Revises: 001
Create Date: 2026-02-24
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "api_request_logs",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "conversation_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("conversations.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("session_id", sa.String(128), nullable=True),
        sa.Column("ip_hash", sa.String(64), nullable=False),
        sa.Column("fingerprint", sa.String(64), nullable=True),
        sa.Column("method", sa.String(16), nullable=False),
        sa.Column("path", sa.String(255), nullable=False),
        sa.Column("request_body", sa.JSON(), nullable=False),
        sa.Column("response_body", sa.Text(), nullable=True),
        sa.Column(
            "status", sa.String(32), nullable=False, server_default="in_progress"
        ),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_api_request_logs_ip_hash", "api_request_logs", ["ip_hash"])
    op.create_index(
        "ix_api_request_logs_conversation_id", "api_request_logs", ["conversation_id"]
    )
    op.create_index(
        "ix_api_request_logs_session_id", "api_request_logs", ["session_id"]
    )
    op.create_index(
        "ix_api_request_logs_fingerprint", "api_request_logs", ["fingerprint"]
    )

    op.create_table(
        "tool_call_logs",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "conversation_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("conversations.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "api_request_log_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("api_request_logs.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("session_id", sa.String(128), nullable=True),
        sa.Column("ip_hash", sa.String(64), nullable=False),
        sa.Column("tool_name", sa.String(128), nullable=False),
        sa.Column("input_payload", sa.JSON(), nullable=False),
        sa.Column("output_preview", sa.Text(), nullable=True),
        sa.Column("cache_hit", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("success", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("duration_ms", sa.Float(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )
    op.create_index("ix_tool_call_logs_tool_name", "tool_call_logs", ["tool_name"])
    op.create_index("ix_tool_call_logs_ip_hash", "tool_call_logs", ["ip_hash"])
    op.create_index("ix_tool_call_logs_session_id", "tool_call_logs", ["session_id"])
    op.create_index(
        "ix_tool_call_logs_conversation_id", "tool_call_logs", ["conversation_id"]
    )
    op.create_index(
        "ix_tool_call_logs_api_request_log_id", "tool_call_logs", ["api_request_log_id"]
    )
    op.create_index("ix_tool_call_logs_created_at", "tool_call_logs", ["created_at"])

    op.create_table(
        "epstein_api_call_logs",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "conversation_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("conversations.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "tool_call_log_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("tool_call_logs.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "api_request_log_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("api_request_logs.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("session_id", sa.String(128), nullable=True),
        sa.Column("ip_hash", sa.String(64), nullable=False),
        sa.Column("endpoint", sa.String(128), nullable=False),
        sa.Column("params_payload", sa.JSON(), nullable=False),
        sa.Column("cache_key", sa.String(128), nullable=False),
        sa.Column("cache_hit", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("response_preview", sa.Text(), nullable=True),
        sa.Column("success", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("duration_ms", sa.Float(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )
    op.create_index(
        "ix_epstein_api_call_logs_endpoint", "epstein_api_call_logs", ["endpoint"]
    )
    op.create_index(
        "ix_epstein_api_call_logs_cache_hit", "epstein_api_call_logs", ["cache_hit"]
    )
    op.create_index(
        "ix_epstein_api_call_logs_ip_hash", "epstein_api_call_logs", ["ip_hash"]
    )
    op.create_index(
        "ix_epstein_api_call_logs_conversation_id",
        "epstein_api_call_logs",
        ["conversation_id"],
    )
    op.create_index(
        "ix_epstein_api_call_logs_api_request_log_id",
        "epstein_api_call_logs",
        ["api_request_log_id"],
    )
    op.create_index(
        "ix_epstein_api_call_logs_tool_call_log_id",
        "epstein_api_call_logs",
        ["tool_call_log_id"],
    )
    op.create_index(
        "ix_epstein_api_call_logs_session_id", "epstein_api_call_logs", ["session_id"]
    )
    op.create_index(
        "ix_epstein_api_call_logs_created_at", "epstein_api_call_logs", ["created_at"]
    )
    op.create_index(
        "ix_epstein_api_call_logs_cache_key", "epstein_api_call_logs", ["cache_key"]
    )

    op.create_table(
        "epstein_api_cache",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("endpoint", sa.String(128), nullable=False),
        sa.Column("params_payload", sa.JSON(), nullable=False),
        sa.Column("cache_key", sa.String(128), nullable=False),
        sa.Column("response_payload", sa.Text(), nullable=False),
        sa.Column("hit_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("cache_key", name="uq_epstein_api_cache_key"),
    )
    op.create_index("ix_epstein_api_cache_endpoint", "epstein_api_cache", ["endpoint"])
    op.create_index(
        "ix_epstein_api_cache_cache_key", "epstein_api_cache", ["cache_key"]
    )
    op.create_index(
        "ix_epstein_api_cache_expires_at", "epstein_api_cache", ["expires_at"]
    )


def downgrade() -> None:
    op.drop_index("ix_epstein_api_cache_expires_at", table_name="epstein_api_cache")
    op.drop_index("ix_epstein_api_cache_cache_key", table_name="epstein_api_cache")
    op.drop_index("ix_epstein_api_cache_endpoint", table_name="epstein_api_cache")
    op.drop_table("epstein_api_cache")

    op.drop_index(
        "ix_epstein_api_call_logs_cache_key", table_name="epstein_api_call_logs"
    )
    op.drop_index(
        "ix_epstein_api_call_logs_created_at", table_name="epstein_api_call_logs"
    )
    op.drop_index(
        "ix_epstein_api_call_logs_session_id", table_name="epstein_api_call_logs"
    )
    op.drop_index(
        "ix_epstein_api_call_logs_tool_call_log_id", table_name="epstein_api_call_logs"
    )
    op.drop_index(
        "ix_epstein_api_call_logs_api_request_log_id",
        table_name="epstein_api_call_logs",
    )
    op.drop_index(
        "ix_epstein_api_call_logs_conversation_id", table_name="epstein_api_call_logs"
    )
    op.drop_index(
        "ix_epstein_api_call_logs_ip_hash", table_name="epstein_api_call_logs"
    )
    op.drop_index(
        "ix_epstein_api_call_logs_cache_hit", table_name="epstein_api_call_logs"
    )
    op.drop_index(
        "ix_epstein_api_call_logs_endpoint", table_name="epstein_api_call_logs"
    )
    op.drop_table("epstein_api_call_logs")

    op.drop_index("ix_tool_call_logs_created_at", table_name="tool_call_logs")
    op.drop_index("ix_tool_call_logs_api_request_log_id", table_name="tool_call_logs")
    op.drop_index("ix_tool_call_logs_conversation_id", table_name="tool_call_logs")
    op.drop_index("ix_tool_call_logs_session_id", table_name="tool_call_logs")
    op.drop_index("ix_tool_call_logs_ip_hash", table_name="tool_call_logs")
    op.drop_index("ix_tool_call_logs_tool_name", table_name="tool_call_logs")
    op.drop_table("tool_call_logs")

    op.drop_index("ix_api_request_logs_fingerprint", table_name="api_request_logs")
    op.drop_index("ix_api_request_logs_session_id", table_name="api_request_logs")
    op.drop_index("ix_api_request_logs_conversation_id", table_name="api_request_logs")
    op.drop_index("ix_api_request_logs_ip_hash", table_name="api_request_logs")
    op.drop_table("api_request_logs")
