"""PostgreSQL-backed query service for the production API boundary."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

TABLES={
    "entities":"world_intelligence.entities",
    "events":"world_intelligence.events",
    "world-state":"world_intelligence.temporal_assertions",
    "changes":"world_intelligence.changes",
    "signals":"world_intelligence.signals",
    "evidence":"world_intelligence.evidence",
    "provenance":"world_intelligence.provenance_records",
}

@dataclass
class PostgresQueryService:
    pool: Any

    def query(self, resource:str, *, cursor:int=0, limit:int=100, **_:Any):
        if resource not in TABLES:
            raise KeyError(resource)
        if cursor<0 or limit<1 or limit>1000:
            raise ValueError("invalid pagination")
        table=TABLES[resource]
        with self.pool.connection() as connection:
            rows=connection.execute(
                f"SELECT to_jsonb(row) FROM (SELECT * FROM {table} ORDER BY id LIMIT %s OFFSET %s) row",
                (limit,cursor),
            ).fetchall()
            total=connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        items=[row[0] for row in rows]
        next_cursor=str(cursor+len(items)) if cursor+len(items)<total else None
        from packages.contracts.api import QueryPage
        return QueryPage(items,next_cursor,total)
