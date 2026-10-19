"""PostgreSQL query service with fail-closed tenant policy and append-only access auditing."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from packages.contracts.api import QueryContext, QueryPage
from api.query.service import RESOURCE_CAPABILITIES

TABLES = {
    "entities": "world_intelligence.entities",
    "events": "world_intelligence.events",
    "world-state": "world_intelligence.temporal_assertions",
    "changes": "world_intelligence.changes",
    "signals": "world_intelligence.signals",
    "evidence": "world_intelligence.evidence",
    "provenance": "world_intelligence.provenance_records",
    "regions": "world_intelligence.geofences",
}

@dataclass
class PostgresQueryService:
    pool: Any

    def query(
        self,
        resource: str,
        *,
        context: QueryContext | None = None,
        cursor: int = 0,
        limit: int = 100,
        **_: Any,
    ) -> QueryPage:
        if resource not in TABLES:
            raise KeyError(resource)
        if cursor < 0 or limit < 1 or limit > 1000:
            raise ValueError("invalid pagination")
        capability = RESOURCE_CAPABILITIES[resource]
        if context is None or not context.tenant_id or not context.subject_id or not context.purpose:
            raise PermissionError("query context required")

        with self.pool.connection() as connection:
            policy = connection.execute(
                "SELECT allowed_capabilities, allowed_purposes "
                "FROM world_intelligence.tenant_policies WHERE tenant_id = %s",
                (context.tenant_id,),
            ).fetchone()
            allowed_capabilities, allowed_purposes = policy if policy else ([], [])
            allowed = capability in (allowed_capabilities or []) and context.purpose in (allowed_purposes or [])
            outcome = "allowed" if allowed else "denied"
            connection.execute(
                "INSERT INTO world_intelligence.security_audit_events "
                "(actor_id, tenant_id, action, outcome, occurred_at, metadata) "
                "VALUES (%s, %s, %s, %s, %s, %s::jsonb)",
                (
                    context.subject_id,
                    context.tenant_id,
                    f"query:{resource}",
                    outcome,
                    datetime.now(timezone.utc),
                    json.dumps({
                        "capability": capability,
                        "purpose": context.purpose,
                        "request_id": context.request_id,
                        "traceparent": context.traceparent,
                    }),
                ),
            )
            if allowed:
                table = TABLES[resource]
                if resource == "regions":
                    rows = connection.execute(
                        "SELECT jsonb_build_object('id', id, 'name', name, 'geometry', ST_AsGeoJSON(geom)::jsonb) "
                        "FROM world_intelligence.geofences ORDER BY id LIMIT %s OFFSET %s",
                        (limit, cursor),
                    ).fetchall()
                else:
                    rows = connection.execute(
                        f"SELECT to_jsonb(row) FROM (SELECT * FROM {table} ORDER BY id LIMIT %s OFFSET %s) row",
                        (limit, cursor),
                    ).fetchall()
                total = connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
            else:
                rows = []
                total = 0
        if not allowed:
            raise PermissionError("tenant policy denied query")
        items = [row[0] for row in rows]
        next_cursor = str(cursor + len(items)) if cursor + len(items) < total else None
        return QueryPage(items, next_cursor, total)
