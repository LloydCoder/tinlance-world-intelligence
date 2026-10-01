"""Small dependency-free HTTP runtime for controlled deployments."""
from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from uuid import uuid4
from api.query.service import IntelligenceQueryService
from api.http.router import IntelligenceRouter
from runtime.auth import authorized
from runtime.config import RuntimeConfig

class RuntimeHandler(BaseHTTPRequestHandler):
    server_version = "TinlanceWorldIntelligence/0.1"

    def _json(self, status: int, payload: dict, request_id: str) -> None:
        body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Request-ID", request_id)
        self.end_headers()
        self.wfile.write(body)

    def _request_id(self) -> str:
        return self.headers.get("X-Request-ID") or str(uuid4())

    def do_GET(self) -> None:
        rid = self._request_id()
        cfg = self.server.runtime_config
        if self.path == "/healthz":
            return self._json(200, {"status": "ok", "service": "world-intelligence"}, rid)
        if self.path == "/readyz":
            return self._json(200, {"status": "ready", "service": "world-intelligence", "environment": cfg.environment}, rid)
        if not authorized(self.headers.get("Authorization"), cfg.bearer_token, required=cfg.require_auth):
            return self._json(401, {"error": "unauthorized"}, rid)
        try:
            page = self.server.router.dispatch(self.path)
            return self._json(200, {"items": page.items, "next_cursor": page.next_cursor, "total": page.total}, rid)
        except KeyError:
            return self._json(404, {"error": "not_found"}, rid)
        except ValueError as exc:
            return self._json(400, {"error": str(exc)}, rid)

    def do_POST(self) -> None:
        rid = self._request_id()
        length = int(self.headers.get("Content-Length", "0") or 0)
        cfg = self.server.runtime_config
        if length > cfg.max_body_bytes:
            return self._json(413, {"error": "request_body_too_large"}, rid)
        return self._json(405, {"error": "method_not_allowed"}, rid)

    def log_message(self, format: str, *args: object) -> None:
        return

class WorldIntelligenceServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, address: tuple[str, int], config: RuntimeConfig, stores: dict[str, list[dict]] | None = None):
        self.runtime_config = config
        self.router = IntelligenceRouter(IntelligenceQueryService(stores or {}))
        super().__init__(address, RuntimeHandler)

def serve(config: RuntimeConfig | None = None) -> None:
    cfg = config or RuntimeConfig.from_env()
    WorldIntelligenceServer((cfg.host, cfg.port), cfg).serve_forever()
