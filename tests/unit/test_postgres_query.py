import unittest

from api.query.postgres import PostgresQueryService
from packages.contracts.api import QueryContext

class Cursor:
    def __init__(self):
        self.sql = ""
        self.args = ()
        self.executed = []
    def execute(self, sql, args=()):
        self.sql, self.args = sql, args
        self.executed.append((sql, args))
        return self
    def fetchall(self):
        return [({"id": "e1"},)]
    def fetchone(self):
        if "allowed_capabilities" in self.sql:
            return (["query_entity", "query_region"], ["account_research"])
        if "count(*)" in self.sql:
            return (1,)
        return None

class Connection:
    def __init__(self):
        self.cursor = Cursor()
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def execute(self, sql, args=()): return self.cursor.execute(sql, args)
    def close(self): pass

class Pool:
    def __init__(self): self.conn = Connection()
    def connection(self): return self.conn

class PostgresQueryTests(unittest.TestCase):
    def setUp(self):
        self.pool = Pool()
        self.service = PostgresQueryService(self.pool)
        self.context = QueryContext(tenant_id="tenant-a", subject_id="subject-a", purpose="account_research")

    def test_allowlisted_resource_requires_matching_tenant_policy(self):
        page = self.service.query("entities", context=self.context, cursor=0, limit=1)
        self.assertEqual(page.items, [{"id": "e1"}])
        self.assertIsNone(page.next_cursor)
        sql = [item[0] for item in self.pool.conn.cursor.executed]
        self.assertTrue(any("tenant_policies" in statement for statement in sql))
        self.assertTrue(any("INSERT INTO world_intelligence.security_audit_events" in statement for statement in sql))

    def test_region_query_uses_geojson_projection(self):
        self.service.query("regions", context=self.context)
        statements = [item[0] for item in self.pool.conn.cursor.executed]
        self.assertTrue(any("ST_AsGeoJSON" in statement for statement in statements))

    def test_unknown_resource_fails_closed(self):
        with self.assertRaises(KeyError):
            self.service.query("passwd", context=self.context)

    def test_missing_query_context_fails_closed(self):
        with self.assertRaises(PermissionError):
            self.service.query("entities")

    def test_disallowed_capability_is_audited_then_denied(self):
        with self.assertRaises(PermissionError):
            self.service.query("evidence", context=self.context)
        statements = [item[0] for item in self.pool.conn.cursor.executed]
        self.assertTrue(any("INSERT INTO world_intelligence.security_audit_events" in statement for statement in statements))

if __name__ == "__main__":
    unittest.main()
