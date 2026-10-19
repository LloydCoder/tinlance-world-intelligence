import json
import threading
import unittest
from datetime import UTC, datetime, timedelta
from http.client import HTTPConnection

from runtime.config import RuntimeConfig
from runtime.server import WorldIntelligenceServer
from runtime.platform_token import PlatformPrincipal

class RuntimeHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cfg = RuntimeConfig(host="127.0.0.1", port=0, bearer_token="test-token", require_auth=True)
        cls.server = WorldIntelligenceServer(
            ("127.0.0.1", 0),
            cfg,
            {"entities": [{"id": "e1"}], "evidence": [{"id": "evidence-1"}], "regions": [{"id": "r1", "name": "Region One"}]},
            tenant_policies={
                "tenant-a": {
                    "allowed_capabilities": ["query_entity", "query_region"],
                    "allowed_purposes": ["account_research"],
                }
            },
        )
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.port = cls.server.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def get(self, path, auth=True, tenant="tenant-a", subject="subject-1", purpose="account_research"):
        connection = HTTPConnection("127.0.0.1", self.port)
        headers = {"Authorization": "Bearer test-token"} if auth else {}
        if tenant is not None:
            headers["X-Tinlance-Tenant-ID"] = tenant
        if subject is not None:
            headers["X-Tinlance-Subject-ID"] = subject
        if purpose is not None:
            headers["X-Tinlance-Purpose"] = purpose
        headers["traceparent"] = "00-0123456789abcdef0123456789abcdef-0123456789abcdef-01"
        connection.request("GET", path, headers=headers)
        response = connection.getresponse()
        data = json.loads(response.read())
        connection.close()
        return response.status, data

    def test_health_is_public(self):
        self.assertEqual(self.get("/healthz", False)[0], 200)

    def test_readiness_is_public(self):
        self.assertEqual(self.get("/readyz", False)[0], 200)

    def test_api_requires_auth(self):
        self.assertEqual(self.get("/v1/entities", False)[0], 401)

    def test_api_returns_query_page(self):
        status, data = self.get("/v1/entities")
        self.assertEqual(status, 200)
        self.assertEqual(data["items"], [{"id": "e1"}])

    def test_query_requires_scoped_context(self):
        self.assertEqual(self.get("/v1/entities", tenant=None)[0], 400)
        self.assertEqual(self.get("/v1/entities", subject=None)[0], 400)
        self.assertEqual(self.get("/v1/entities", purpose=None)[0], 400)

    def test_region_query_is_a_registered_capability(self):
        status, body = self.get("/v1/regions")
        self.assertEqual(status, 200, body)
        self.assertEqual(body["items"][0]["id"], "r1")

    def test_tenant_without_policy_is_denied(self):
        self.assertEqual(self.get("/v1/entities", tenant="tenant-b")[0], 403)

    def test_capability_and_purpose_are_enforced_per_route(self):
        self.assertEqual(self.get("/v1/evidence")[0], 403)
        self.assertEqual(self.get("/v1/entities", purpose="marketing")[0], 403)

    def test_query_access_is_audited(self):
        events = self.server.router.service.audit_events
        self.assertTrue(any(item["action"] == "query:entities" and item["outcome"] == "allowed" for item in events))
        self.assertTrue(any(item["action"] == "query:evidence" and item["outcome"] == "denied" for item in events))

    def test_unknown_route(self):
        self.assertEqual(self.get("/v1/nope")[0], 404)

    def test_query_identity_is_derived_from_platform_token_not_headers(self):
        class FakeVerifier:
            def verify(self, token):
                if token != "platform-token":
                    raise PermissionError("invalid token")
                return PlatformPrincipal(
                    tenant_id="tenant-a",
                    subject_id="subject-1",
                    client_id="platform-client",
                    principal_type="agent",
                    token_id="token-1",
                    scopes=frozenset({"world-intelligence:query"}),
                    purpose="account_research",
                    request_id="platform-identity-test",
                    traceparent="00-0123456789abcdef0123456789abcdef-0123456789abcdef-01",
                    expires_at=datetime.now(UTC) + timedelta(minutes=2),
                )

        cfg = RuntimeConfig(host="127.0.0.1", port=0, bearer_token=None, require_auth=True)
        server = WorldIntelligenceServer(
            ("127.0.0.1", 0),
            cfg,
            {"entities": [{"id": "e1"}]},
            tenant_policies={"tenant-a": {"allowed_capabilities": ["query_entity"], "allowed_purposes": ["account_research"]}},
            token_verifier=FakeVerifier(),
        )
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            def request(tenant_header=None, subject_header=None, purpose_header=None, request_id_header=None, traceparent_header=None):
                connection = HTTPConnection("127.0.0.1", server.server_address[1], timeout=5)
                headers = {"Authorization": "Bearer platform-token", "X-Tinlance-Purpose": "account_research", "X-Request-ID": "platform-identity-test", "traceparent": "00-0123456789abcdef0123456789abcdef-0123456789abcdef-01"}
                if tenant_header is not None:
                    headers["X-Tinlance-Tenant-ID"] = tenant_header
                if subject_header is not None:
                    headers["X-Tinlance-Subject-ID"] = subject_header
                if purpose_header is not None:
                    headers["X-Tinlance-Purpose"] = purpose_header
                if request_id_header is not None:
                    headers["X-Request-ID"] = request_id_header
                if traceparent_header is not None:
                    headers["traceparent"] = traceparent_header
                connection.request("GET", "/v1/entities", headers=headers)
                response = connection.getresponse()
                status = response.status
                body = json.loads(response.read())
                connection.close()
                return status, body

            status, body = request()
            self.assertEqual(status, 200, body)
            status, body = request("tenant-b")
            self.assertEqual(status, 403, body)
            self.assertEqual(body.get("error"), "identity_context_mismatch")
            status, body = request(subject_header="subject-b")
            self.assertEqual(status, 403, body)
            self.assertEqual(body.get("error"), "identity_context_mismatch")
            status, body = request(purpose_header="marketing")
            self.assertEqual(status, 403, body)
            self.assertEqual(body.get("error"), "identity_context_mismatch")
            status, body = request(request_id_header="other-request-id")
            self.assertEqual(status, 403, body)
            self.assertEqual(body.get("error"), "identity_context_mismatch")
            status, body = request(traceparent_header="00-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-bbbbbbbbbbbbbbbb-01")
            self.assertEqual(status, 403, body)
            self.assertEqual(body.get("error"), "identity_context_mismatch")
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

if __name__ == "__main__":
    unittest.main()
