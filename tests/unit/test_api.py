import unittest

from api.http.router import IntelligenceRouter
from api.query.service import IntelligenceQueryService
from packages.contracts.api import QueryContext

class ApiTests(unittest.TestCase):
    def test_page(self):
        service = IntelligenceQueryService(
            {"entities": [{"id": "1"}, {"id": "2"}]},
            tenant_policies={
                "tenant-a": {
                    "allowed_capabilities": ["query_entity"],
                    "allowed_purposes": ["account_research"],
                }
            },
        )
        context = QueryContext(tenant_id="tenant-a", subject_id="subject-a", purpose="account_research")
        page = IntelligenceRouter(service).dispatch("/v1/entities", 1, context=context)
        self.assertEqual(page.items, [{"id": "1"}])
        self.assertEqual(page.next_cursor, "1")
        self.assertEqual(page.total, 2)

if __name__ == "__main__":
    unittest.main()
