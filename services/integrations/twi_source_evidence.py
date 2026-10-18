"""Authenticated intake of TWI source-evidence candidates.

These records are not canonical observations or truth assertions. World Intelligence keeps
them as candidate evidence for later governed normalization and correlation.
"""

from __future__ import annotations

import hashlib
import json
import re
import threading
import unicodedata
import uuid
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlsplit


class SourceEvidenceValidationError(ValueError):
    """The source-evidence envelope violates its versioned contract."""


class IdempotencyConflictError(ValueError):
    """An idempotency key was reused for a different payload."""


_HEX_64 = re.compile(r"^[0-9a-f]{64}$")
_CLAIM_ID = re.compile(r"^[A-Za-z0-9._:-]{1,64}$")
_IDEMPOTENCY_KEY = re.compile(r"^[A-Za-z0-9._:-]{16,128}$")
_TRACEPARENT = re.compile(r"^[0-9a-f]{2}-[0-9a-f]{32}-[0-9a-f]{16}-[0-9a-f]{2}$")
_ALLOWED_FIELDS = {
    "schema_version",
    "source_system",
    "tenant_ref",
    "source_job_id",
    "claim_id",
    "statement",
    "source_url",
    "retrieved_at",
    "media_type",
    "artifact_sha256",
    "quote",
    "quote_sha256",
    "verifier_version",
    "report_sha256",
}


def normalize_quote(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).split())


def _required_text(payload: dict[str, Any], key: str, *, maximum: int) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise SourceEvidenceValidationError(f"invalid {key}")
    if value != value.strip():
        raise SourceEvidenceValidationError(f"invalid {key}")
    return value


def validate_envelope(payload: object, idempotency_key: str, traceparent: str | None) -> dict[str, Any]:
    if not isinstance(payload, dict) or set(payload) != _ALLOWED_FIELDS:
        raise SourceEvidenceValidationError("source-evidence envelope has unexpected fields")
    if not _IDEMPOTENCY_KEY.fullmatch(idempotency_key):
        raise SourceEvidenceValidationError("invalid idempotency key")
    if traceparent is not None:
        if not _TRACEPARENT.fullmatch(traceparent):
            raise SourceEvidenceValidationError("invalid traceparent")
        version, trace_id, span_id, _flags = traceparent.split("-")
        if version == "ff" or set(trace_id) == {"0"} or set(span_id) == {"0"}:
            raise SourceEvidenceValidationError("invalid traceparent identifiers")

    if payload.get("schema_version") != "1.0.0":
        raise SourceEvidenceValidationError("unsupported source-evidence schema version")
    if payload.get("source_system") != "tinlance-web-intelligence":
        raise SourceEvidenceValidationError("unsupported source system")
    tenant_ref = _required_text(payload, "tenant_ref", maximum=64)
    if not _HEX_64.fullmatch(tenant_ref):
        raise SourceEvidenceValidationError("tenant_ref must be a pseudonymous SHA-256 reference")
    _required_text(payload, "source_job_id", maximum=64)
    claim_id = _required_text(payload, "claim_id", maximum=64)
    if not _CLAIM_ID.fullmatch(claim_id):
        raise SourceEvidenceValidationError("invalid claim_id")
    _required_text(payload, "statement", maximum=500)

    source_url = _required_text(payload, "source_url", maximum=4096)
    parsed = urlsplit(source_url)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
    ):
        raise SourceEvidenceValidationError("invalid source_url")

    retrieved_at = _required_text(payload, "retrieved_at", maximum=64)
    try:
        timestamp = datetime.fromisoformat(retrieved_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SourceEvidenceValidationError("invalid retrieved_at") from exc
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise SourceEvidenceValidationError("retrieved_at must be timezone-aware")

    _required_text(payload, "media_type", maximum=128)
    for key in ("artifact_sha256", "quote_sha256", "report_sha256"):
        value = _required_text(payload, key, maximum=64)
        if not _HEX_64.fullmatch(value):
            raise SourceEvidenceValidationError(f"invalid {key}")
    quote = _required_text(payload, "quote", maximum=350)
    normalized_quote = normalize_quote(quote)
    if len(normalized_quote) < 8:
        raise SourceEvidenceValidationError("quote must contain at least 8 normalized characters")
    if hashlib.sha256(normalized_quote.encode("utf-8")).hexdigest() != payload["quote_sha256"]:
        raise SourceEvidenceValidationError("quote_sha256 does not match quote")
    verifier_version = _required_text(payload, "verifier_version", maximum=64)
    if not re.fullmatch(r"twi-citation-verifier/[0-9]+\.[0-9]+\.[0-9]+", verifier_version):
        raise SourceEvidenceValidationError("invalid verifier_version")

    # Normalize the timestamp and quote so equivalent retries have stable payload hashes.
    validated = dict(payload)
    validated["retrieved_at"] = timestamp.astimezone(UTC).isoformat()
    validated["quote"] = normalized_quote
    return validated


def payload_digest(payload: dict[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


class InMemorySourceEvidenceStore:
    """Thread-safe development/test store; not a production persistence backend."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._records: dict[tuple[str, str], dict[str, Any]] = {}

    def ingest(
        self,
        payload: dict[str, Any],
        *,
        idempotency_key: str,
        request_id: str,
        traceparent: str | None,
    ) -> dict[str, Any]:
        digest = payload_digest(payload)
        key = (payload["tenant_ref"], idempotency_key)
        with self._lock:
            existing = self._records.get(key)
            if existing is not None:
                if existing["payload_sha256"] != digest:
                    raise IdempotencyConflictError("idempotency key was used with another payload")
                return {
                    "evidence_id": existing["evidence_id"],
                    "status": existing["status"],
                    "replayed": True,
                }
            evidence_id = str(uuid.uuid4())
            self._records[key] = {
                **payload,
                "evidence_id": evidence_id,
                "payload_sha256": digest,
                "idempotency_key": idempotency_key,
                "request_id": request_id,
                "traceparent": traceparent,
                "status": "candidate",
            }
            return {"evidence_id": evidence_id, "status": "candidate", "replayed": False}


class PostgresSourceEvidenceStore:
    """PostgreSQL implementation backed by the runtime's existing connection pool."""

    def __init__(self, pool: Any) -> None:
        self._pool = pool

    def ingest(
        self,
        payload: dict[str, Any],
        *,
        idempotency_key: str,
        request_id: str,
        traceparent: str | None,
    ) -> dict[str, Any]:
        digest = payload_digest(payload)
        with self._pool.connection() as connection:
            inserted = connection.execute(
                """
                INSERT INTO world_intelligence.external_source_evidence (
                    source_system, tenant_ref, source_job_id, claim_id, statement,
                    source_url, retrieved_at, media_type, artifact_sha256, quote,
                    quote_sha256, verifier_version, report_sha256, idempotency_key,
                    payload_sha256, request_id, traceparent
                ) VALUES (
                    %(source_system)s, %(tenant_ref)s, %(source_job_id)s, %(claim_id)s,
                    %(statement)s, %(source_url)s, %(retrieved_at)s, %(media_type)s,
                    %(artifact_sha256)s, %(quote)s, %(quote_sha256)s, %(verifier_version)s,
                    %(report_sha256)s, %(idempotency_key)s, %(payload_sha256)s,
                    %(request_id)s, %(traceparent)s
                )
                ON CONFLICT (tenant_ref, idempotency_key) DO NOTHING
                RETURNING id::text
                """,
                {
                    **payload,
                    "idempotency_key": idempotency_key,
                    "payload_sha256": digest,
                    "request_id": request_id,
                    "traceparent": traceparent,
                },
            ).fetchone()
            if inserted is not None:
                return {"evidence_id": inserted[0], "status": "candidate", "replayed": False}
            existing = connection.execute(
                """
                SELECT id::text, payload_sha256, status
                FROM world_intelligence.external_source_evidence
                WHERE tenant_ref = %s AND idempotency_key = %s
                """,
                (payload["tenant_ref"], idempotency_key),
            ).fetchone()
            if existing is None:
                raise RuntimeError("idempotent source-evidence row disappeared after conflict")
            if existing[1] != digest:
                raise IdempotencyConflictError("idempotency key was used with another payload")
            return {"evidence_id": existing[0], "status": existing[2], "replayed": True}
