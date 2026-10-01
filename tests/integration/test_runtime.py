import json
import threading
import unittest
from http.client import HTTPConnection

from runtime.config import RuntimeConfig
from runtime.server import WorldIntelligenceServer

class RuntimeHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cfg = RuntimeConfig(host="127.0.0.1", port=0, bearer_token="test-token", require_auth=True)
        cls.server = WorldIntelligenceServer(("127.0.0.1", 0), cfg, {"entities": [{"id": "e1"}]})
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.port = cls.server.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def get(self, path, auth=True):
        connection = HTTPConnection("127.0.0.1", self.port)
        headers = {"Authorization": "Bearer test-token"} if auth else {}
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

    def test_unknown_route(self):
        self.assertEqual(self.get("/v1/nope")[0], 404)

if __name__ == "__main__":
    unittest.main()
