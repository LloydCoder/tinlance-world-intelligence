"""Bounded HTTP runtime for controlled deployments."""

from __future__ import annotations

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from uuid import uuid4

from api.http.router import IntelligenceRouter
from api.query.postgres import PostgresQueryService
from api.query.service import IntelligenceQueryService
from runtime.auth import authorized
from runtime.config import RuntimeConfig
from runtime.rate_limit import FixedWindowLimiter
from services.integrations.twi_source_evidence import (
    IdempotencyConflictError,
    InMemorySourceEvidenceStore,
    PostgresSourceEvidenceStore,
    SourceEvidenceValidationError,
    validate_envelope,
)


_REQUEST_ID = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")


def _reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


class RuntimeHandler(BaseHTTPRequestHandler):
    server_version = "TinlanceWorldIntelligence/0.3"

    def _json(self, status: int, payload: dict, request_id: str) -> None:
        body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Request-ID", request_id)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _request_id(self) -> str:
        value = self.headers.get("X-Request-ID", "")
        return value if _REQUEST_ID.fullmatch(value) else str(uuid4())

    def _authorized(self, request_id: str, *, source_evidence: bool = False) -> bool:
        cfg = self.server.runtime_config
        expected_token = cfg.source_evidence_bearer_token if source_evidence else cfg.bearer_token
        required = True if source_evidence else cfg.require_auth
        if not authorized(self.headers.get("Authorization"), expected_token, required=required):
            self._json(401, {"error": "unauthorized"}, request_id)
            return False
        key = self.headers.get("Authorization") or self.client_address[0]
        if not self.server.rate_limiter.allow(key):
            self._json(429, {"error": "rate_limited"}, request_id)
            return False
        return True

    def do_GET(self) -> None:
        request_id = self._request_id()
        cfg = self.server.runtime_config
        if self.path == "/healthz":
            return self._json(200, {"status": "ok", "service": "world-intelligence"}, request_id)
        if self.path == "/readyz":
            return self._json(
                200,
                {
                    "status": "ready",
                    "service": "world-intelligence",
                    "environment": cfg.environment,
                    "storage": cfg.storage_mode,
                },
                request_id,
            )
        if not self._authorized(request_id):
            return
        try:
            page = self.server.router.dispatch(self.path)
            return self._json(
                200,
                {"items": page.items, "next_cursor": page.next_cursor, "total": page.total},
                request_id,
            )
        except KeyError:
            return self._json(404, {"error": "not_found"}, request_id)
        except ValueError:
            return self._json(400, {"error": "invalid_request"}, request_id)

    def do_POST(self) -> None:
        request_id = self._request_id()
        if self.path != "/v1/source-evidence":
            return self._json(405, {"error": "method_not_allowed"}, request_id)

        raw_length = self.headers.get("Content-Length")
        if raw_length is None:
            return self._json(411, {"error": "content_length_required"}, request_id)
        try:
            length = int(raw_length)
        except ValueError:
            return self._json(400, {"error": "invalid_content_length"}, request_id)
        if length <= 0:
            return self._json(400, {"error": "empty_request_body"}, request_id)
        if length > self.server.runtime_config.max_body_bytes:
            return self._json(413, {"error": "request_body_too_large"}, request_id)
        if self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower() != "application/json":
            return self._json(415, {"error": "application_json_required"}, request_id)
        if not self._authorized(request_id, source_evidence=True):
            return

        body = self.rfile.read(length)
        if len(body) != length:
            return self._json(400, {"error": "incomplete_request_body"}, request_id)
        try:
            payload = json.loads(body, object_pairs_hook=_reject_duplicate_json_keys)
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
            return self._json(400, {"error": "invalid_json"}, request_id)

        idempotency_key = self.headers.get("Idempotency-Key", "")
        traceparent = self.headers.get("traceparent")
        try:
            validated = validate_envelope(payload, idempotency_key, traceparent)
            result = self.server.evidence_store.ingest(
                validated,
                idempotency_key=idempotency_key,
                request_id=request_id,
                traceparent=traceparent,
            )
        except SourceEvidenceValidationError:
            return self._json(422, {"error": "invalid_source_evidence"}, request_id)
        except IdempotencyConflictError:
            return self._json(409, {"error": "idempotency_conflict"}, request_id)
        except Exception:
            return self._json(503, {"error": "source_evidence_store_unavailable"}, request_id)

        status = 200 if result["replayed"] else 201
        return self._json(status, result, request_id)

    def log_message(self, format: str, *args: object) -> None:
        return


class WorldIntelligenceServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(
        self,
        address: tuple[str, int],
        config: RuntimeConfig,
        stores: dict[str, list[dict]] | None = None,
    ):
        self.runtime_config = config
        self.rate_limiter = FixedWindowLimiter(config.rate_limit_per_minute)
        self.pool = None
        if config.storage_mode == "postgres":
            if not config.database_url:
                raise ValueError("DATABASE_URL is required for PostgreSQL storage")
            try:
                from psycopg_pool import ConnectionPool
            except ImportError as exc:
                raise RuntimeError(
                    "install the runtime dependency with: pip install 'tinlance-world-intelligence[runtime]'"
                ) from exc
            self.pool = ConnectionPool(
                config.database_url,
                min_size=1,
                max_size=10,
                open=True,
                check=ConnectionPool.check_connection,
            )
            service = PostgresQueryService(self.pool)
            self.evidence_store = PostgresSourceEvidenceStore(self.pool)
        else:
            service = IntelligenceQueryService(stores or {})
            self.evidence_store = InMemorySourceEvidenceStore()
        self.router = IntelligenceRouter(service)
        super().__init__(address, RuntimeHandler)

    def server_close(self) -> None:
        if self.pool is not None:
            self.pool.close()
        super().server_close()


def serve(config: RuntimeConfig | None = None) -> None:
    cfg = config or RuntimeConfig.from_env()
    WorldIntelligenceServer((cfg.host, cfg.port), cfg).serve_forever()
