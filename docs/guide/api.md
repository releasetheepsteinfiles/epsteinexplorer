# API

> Credits: Erwin Lejeune - 2026-02-24

## Health

- `GET /health`

Simple liveness check for backend availability.

## Chat

- `POST /api/chat`

Request body:

```json
{
  "message": "Who flew with Epstein in 2002?",
  "conversation_id": "optional-conversation-id",
  "fingerprint": "optional-browser-fingerprint"
}
```

Response:

- Server-sent events stream containing incremental assistant output.

## Notes

- No authentication required.
- Anonymous user tracking is persisted in PostgreSQL.
