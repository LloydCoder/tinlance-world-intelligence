from __future__ import annotations

import hashlib
import json
import threading
import unittest
from http.client import HTTPConnection

from runtime.config import RuntimeConfig
from runtime.server import WorldIntelligenceServer


def _payload() -> dict[str, str]:
    quote = "The company launched a new product in October 2026."
    normalized_quote = " ".join(quote.split())
    return {
        "schema_version": "1.0.0",
        "source_system": "tinlance-web-intelligence",
        "tenant_ref": hashlib.sha256(b"opaque-tenant-reference").hexdigest(),
        "source_job_id": "twi-job-0001",
        "claim_id": "product-launch",
        "statement": "The company launched a new product in October 2026.",
        "source_url": "https://example.com/news",
        "source_url_redacted": False,
        "retrieved_at": "2026-10-18T12:00:00+00:00",
        "media_type": "text/html",
        "artifact_sha256": hashlib.sha256(b"raw-html").hexdigest(),
        "quote": quote,
        "quote_sha256": hashlib.sha256(normalized_quote.encode()).hexdigest(),
        "verifier_version": "twi-citation-verifier/1.0.0",
        "report_sha256": hashlib.sha256(b"report").hexdigest(),
    }


class TWISourceEvidenceIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cfg = RuntimeConfig(
            host="127.0.0.1",
            port=0,
            bearer_token="test-token",
            require_auth=True,
            max_body_bytes=1024 * 1024,
        )
        cls.server = WorldIntelligenceServer(("127.0.0.1", 0), cfg)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.port = cls.server.server_address[1]

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def post(
        self,
        payload: object,
        *,
        auth: bool = True,
        idempotency_key: str = "twi-export-idempotency-0001",
        content_type: str = "application/json",
        raw_body: bytes | None = None,
    ) -> tuple[int, dict, dict[str, str]]:
        connection = HTTPConnection("127.0.0.1", self.port)
        body = raw_body if raw_body is not None else json.dumps(payload).encode()
        headers = {
            "Content-Type": content_type,
            "Idempotency-Key": idempotency_key,
            "X-Request-ID": "w5-source-evidence-test",
            "traceparent": "00-0123456789abcdef0123456789abcdef-0123456789abcdef-01",
        }
        if auth:
            headers["Authorization"] = "Bearer test-token"
        connection.request("POST", "/v1/source-evidence", body=body, headers=headers)
        response = connection.getresponse()
        result_body = response.read()
        result_headers = {key.lower(): value for key, value in response.getheaders()}
        connection.close()
        return response.status, json.loads(result_body), result_headers

    def test_ingest_is_authenticated_and_returns_candidate_not_canonical_truth(self) -> None:
        status, payload, headers = self.post(_payload())
        self.assertEqual(status, 201)
        self.assertEqual(payload["status"], "candidate")
        self.assertFalse(payload["replayed"])
        self.assertEqual(len(payload["evidence_id"]), 36)
        self.assertEqual(headers["x-request-id"], "w5-source-evidence-test")

    def test_idempotent_retry_returns_same_evidence_id(self) -> None:
        first_status, first, _ = self.post(_payload())
        replay_status, replay, _ = self.post(_payload())
        self.assertEqual(first_status, 201)
        self.assertEqual(replay_status, 200)
        self.assertEqual(first["evidence_id"], replay["evidence_id"])
        self.assertTrue(replay["replayed"])

    def test_reusing_idempotency_key_for_changed_payload_is_rejected(self) -> None:
        self.assertEqual(self.post(_payload())[0], 201)
        changed = _payload()
        changed["statement"] = "A different statement with the same key."
        status, payload, _ = self.post(changed)
        self.assertEqual(status, 409)
        self.assertEqual(payload["error"], "idempotency_conflict")

    def test_unauthenticated_ingestion_is_rejected(self) -> None:
        status, payload, _ = self.post(_payload(), auth=False)
        self.assertEqual(status, 401)
        self.assertEqual(payload["error"], "unauthorized")

    def test_invalid_hash_and_extra_fields_are_rejected(self) -> None:
        invalid_hash = _payload()
        invalid_hash["quote_sha256"] = "0" * 64
        self.assertEqual(self.post(invalid_hash)[0], 422)
        extra_field = _payload()
        extra_field["raw_html"] = "<html>not allowed</html>"
        self.assertEqual(self.post(extra_field, idempotency_key="twi-export-idempotency-0002")[0], 422)
        unredacted_url = _payload()
        unredacted_url["source_url"] = "https://example.com/?access_token=secret"
        self.assertEqual(
            self.post(unredacted_url, idempotency_key="twi-export-idempotency-0006")[0],
            422,
        )
        redacted_url = _payload()
        redacted_url["source_url"] = "https://example.com/?access_token=%5BREDACTED%5D"
        redacted_url["source_url_redacted"] = True
        self.assertEqual(
            self.post(redacted_url, idempotency_key="twi-export-idempotency-0007")[0],
            201,
        )

    def test_duplicate_json_keys_are_rejected(self) -> None:
        status, payload, _ = self.post(
            {},
            raw_body=b'{"schema_version":"1.0.0","schema_version":"1.0.0"}',
            idempotency_key="twi-export-idempotency-0003",
        )
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"], "invalid_json")

    def test_content_type_and_trace_context_are_validated(self) -> None:
        self.assertEqual(self.post(_payload(), content_type="text/plain")[0], 415)
        status, payload, _ = self.post(
            _payload(),
            idempotency_key="twi-export-idempotency-0004",
        )
        self.assertEqual(status, 201)
        invalid_trace = {
            "traceparent": "00-00000000000000000000000000000000-0123456789abcdef-01"
        }
        connection = HTTPConnection("127.0.0.1", self.port)
        body = json.dumps(_payload()).encode()
        headers = {
            "Authorization": "Bearer test-token",
            "Content-Type": "application/json",
            "Idempotency-Key": "twi-export-idempotency-0005",
            **invalid_trace,
        }
        connection.request("POST", "/v1/source-evidence", body=body, headers=headers)
        response = connection.getresponse()
        result = json.loads(response.read())
        connection.close()
        self.assertEqual(response.status, 422)
        self.assertEqual(result["error"], "invalid_source_evidence")


if __name__ == "__main__":
    unittest.main()
