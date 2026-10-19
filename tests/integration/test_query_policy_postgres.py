from __future__ import annotations

import json
import os
import uuid

import pytest
from psycopg_pool import ConnectionPool

from api.query.postgres import PostgresQueryService
from packages.contracts.api import QueryContext


def test_postgres_query_requires_tenant_capability_and_purpose_policy() -> None:
    dsn = os.environ.get("WORLD_INTELLIGENCE_TEST_DATABASE_URL")
    if not dsn:
        pytest.skip("canonical ecosystem gate supplies a migrated PostgreSQL database")
    tenant_id = "tenant-policy-" + uuid.uuid4().hex
    subject_id = "subject-policy-" + uuid.uuid4().hex
    with ConnectionPool(dsn, min_size=1, max_size=2, open=True) as pool:
        with pool.connection() as connection:
            connection.execute(
                "INSERT INTO world_intelligence.tenant_policies "
                "(tenant_id, allowed_capabilities, allowed_purposes) "
                "VALUES (%s, %s::jsonb, %s::jsonb)",
                (tenant_id, json.dumps(["query_entity"]), json.dumps(["account_research"])),
            )
        service = PostgresQueryService(pool)
        allowed = service.query(
            "entities",
            context=QueryContext(
                tenant_id=tenant_id,
                subject_id=subject_id,
                purpose="account_research",
                request_id="query-policy-e2e",
            ),
        )
        assert isinstance(allowed.items, list)
        with pytest.raises(PermissionError):
            service.query(
                "evidence",
                context=QueryContext(
                    tenant_id=tenant_id,
                    subject_id=subject_id,
                    purpose="account_research",
                    request_id="query-policy-denied",
                ),
            )
        with pool.connection() as connection:
            outcomes = connection.execute(
                "SELECT action, outcome FROM world_intelligence.security_audit_events "
                "WHERE tenant_id = %s ORDER BY occurred_at",
                (tenant_id,),
            ).fetchall()
        assert ("query:entities", "allowed") in outcomes
        assert ("query:evidence", "denied") in outcomes
