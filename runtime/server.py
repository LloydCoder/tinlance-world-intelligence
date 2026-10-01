"""Bounded HTTP runtime for controlled deployments."""
from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from uuid import uuid4
from api.http.router import IntelligenceRouter
from api.query.service import IntelligenceQueryService
from api.query.postgres import PostgresQueryService
from runtime.auth import authorized
from runtime.config import RuntimeConfig
from runtime.rate_limit import FixedWindowLimiter

class RuntimeHandler(BaseHTTPRequestHandler):
    server_version="TinlanceWorldIntelligence/0.2"

    def _json(self,status:int,payload:dict,request_id:str)->None:
        body=json.dumps(payload,separators=(",",":"),sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(body)))
        self.send_header("X-Request-ID",request_id)
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("Referrer-Policy","no-referrer")
        self.send_header("Cache-Control","no-store")
        self.end_headers()
        self.wfile.write(body)

    def _request_id(self)->str:
        return self.headers.get("X-Request-ID") or str(uuid4())

    def _authorized(self,rid:str)->bool:
        cfg=self.server.runtime_config
        if not authorized(self.headers.get("Authorization"),cfg.bearer_token,required=cfg.require_auth):
            self._json(401,{"error":"unauthorized"},rid); return False
        key=self.headers.get("Authorization") or self.client_address[0]
        if not self.server.rate_limiter.allow(key):
            self._json(429,{"error":"rate_limited"},rid); return False
        return True

    def do_GET(self)->None:
        rid=self._request_id(); cfg=self.server.runtime_config
        if self.path=="/healthz": return self._json(200,{"status":"ok","service":"world-intelligence"},rid)
        if self.path=="/readyz": return self._json(200,{"status":"ready","service":"world-intelligence","environment":cfg.environment,"storage":cfg.storage_mode},rid)
        if not self._authorized(rid): return
        try:
            page=self.server.router.dispatch(self.path)
            return self._json(200,{"items":page.items,"next_cursor":page.next_cursor,"total":page.total},rid)
        except KeyError: return self._json(404,{"error":"not_found"},rid)
        except ValueError as exc: return self._json(400,{"error":str(exc)},rid)

    def do_POST(self)->None:
        rid=self._request_id()
        try: length=int(self.headers.get("Content-Length","0") or 0)
        except ValueError: return self._json(400,{"error":"invalid_content_length"},rid)
        if length>self.server.runtime_config.max_body_bytes:
            return self._json(413,{"error":"request_body_too_large"},rid)
        return self._json(405,{"error":"method_not_allowed"},rid)

    def log_message(self,format:str,*args:object)->None: return

class WorldIntelligenceServer(ThreadingHTTPServer):
    allow_reuse_address=True
    daemon_threads=True

    def __init__(self,address:tuple[str,int],config:RuntimeConfig,stores:dict[str,list[dict]]|None=None):
        self.runtime_config=config
        self.rate_limiter=FixedWindowLimiter(config.rate_limit_per_minute)
        self.pool=None
        if config.storage_mode=="postgres":
            if not config.database_url: raise ValueError("DATABASE_URL is required for PostgreSQL storage")
            try:
                from psycopg_pool import ConnectionPool
            except ImportError as exc:
                raise RuntimeError("install the runtime dependency with: pip install 'tinlance-world-intelligence[runtime]'") from exc
            self.pool=ConnectionPool(config.database_url,min_size=1,max_size=10,open=True,check=ConnectionPool.check_connection)
            service=PostgresQueryService(self.pool)
        else:
            service=IntelligenceQueryService(stores or {})
        self.router=IntelligenceRouter(service)
        super().__init__(address,RuntimeHandler)

    def server_close(self):
        if self.pool is not None: self.pool.close()
        super().server_close()

def serve(config:RuntimeConfig|None=None)->None:
    cfg=config or RuntimeConfig.from_env()
    WorldIntelligenceServer((cfg.host,cfg.port),cfg).serve_forever()
