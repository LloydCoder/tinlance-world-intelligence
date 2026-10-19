from __future__ import annotations

import json
import os
import threading
import unittest
import uuid
from http.client import HTTPConnection

from psycopg_pool import ConnectionPool

from runtime.config import RuntimeConfig
from runtime.server import WorldIntelligenceServer


@unittest.skipUnless(
    os.environ.get("WORLD_INTELLIGENCE_TEST_DATABASE_URL"),
    "canonical ecosystem gate supplies a migrated PostgreSQL database",
)
class PostgresQueryPolicyHTTPTests(unittest.TestCase):
    def test_http_query_enforces_tenant_capability_purpose_and_audit(self) -> None:
        dsn = os.environ["WORLD_INTELLIGENCE_TEST_DATABASE_URL"]
        tenant_id = "tenant-policy-" + uuid.uuid4().hex
        subject_id = "subject-policy-" + uuid.uuid4().hex
        with ConnectionPool(dsn, min_size=1, max_size=2, open=True) as pool:
            with pool.connection() as connection:
                connection.execute(
                    "INSERT INTO world_intelligence.tenant_policies "
                    "(tenant_id, allowed_capabilities, allowed_purposes) "
                    "VALUES (%s, %s::jsonb, %s::jsonb)",
                    (tenant_id, json.dumps(["query_entity", "query_region"]), json.dumps(["account_research"])),
                )

        region_name = "region-e2e-" + uuid.uuid4().hex
        with ConnectionPool(dsn, min_size=1, max_size=2, open=True) as pool:
            with pool.connection() as connection:
                connection.execute(
                    "INSERT INTO world_intelligence.geofences (name, geom) "
                    "VALUES (%s, ST_GeomFromText(%s, 4326))",
                    (region_name, "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"),
                )

        config = RuntimeConfig(
            host="127.0.0.1",
            port=0,
            bearer_token="test-query-service-token",
            require_auth=True,
            storage_mode="postgres",
            database_url=dsn,
        )
        server = WorldIntelligenceServer(("127.0.0.1", 0), config)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        port = server.server_address[1]

        def get(path: str, *, tenant: str | None = tenant_id, purpose: str | None = "account_research"):
            connection = HTTPConnection("127.0.0.1", port, timeout=5)
            headers = {"Authorization": "Bearer test-query-service-token", "X-Tinlance-Subject-ID": subject_id}
            if tenant is not None:
                headers["X-Tinlance-Tenant-ID"] = tenant
            if purpose is not None:
                headers["X-Tinlance-Purpose"] = purpose
            headers["X-Request-ID"] = "query-policy-http-e2e"
            headers["traceparent"] = "00-0123456789abcdef0123456789abcdef-0123456789abcdef-01"
            connection.request("GET", path, headers=headers)
            response = connection.getresponse()
            payload = json.loads(response.read())
            status = response.status
            connection.close()
            return status, payload

        try:
            status, body = get("/v1/entities")
            self.assertEqual(status, 200, body)
            self.assertIn("items", body)

            status, body = get("/v1/regions")
            self.assertEqual(status, 200, body)
            self.assertTrue(any(item.get("name") == region_name and item.get("geometry", {}).get("type") == "Polygon" for item in body["items"]))

            status, body = get("/v1/evidence")
            self.assertEqual(status, 403, body)
            self.assertEqual(body.get("error"), "forbidden")

            status, body = get("/v1/entities", purpose="marketing")
            self.assertEqual(status, 403, body)

            status, body = get("/v1/entities", tenant=None)
            self.assertEqual(status, 400, body)
            self.assertEqual(body.get("error"), "query_context_required")

            status, body = get("/v1/entities", tenant="tenant-without-policy")
            self.assertEqual(status, 403, body)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

        with ConnectionPool(dsn, min_size=1, max_size=2, open=True) as pool:
            with pool.connection() as connection:
                outcomes = connection.execute(
                    "SELECT action, outcome FROM world_intelligence.security_audit_events "
                    "WHERE tenant_id = %s ORDER BY occurred_at",
                    (tenant_id,),
                ).fetchall()
        self.assertIn(("query:entities", "allowed"), outcomes)
        self.assertIn(("query:evidence", "denied"), outcomes)
        self.assertIn(("query:entities", "denied"), outcomes)

if __name__ == "__main__":
    unittest.main()
