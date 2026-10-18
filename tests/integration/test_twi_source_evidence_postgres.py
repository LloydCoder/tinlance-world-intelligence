from __future__ import annotations

import hashlib
import os
import unittest
import uuid

from services.integrations.twi_source_evidence import (
    IdempotencyConflictError,
    PostgresSourceEvidenceStore,
)


def _payload(tenant_ref: str, source_job_id: str) -> dict[str, str]:
    quote = "A verified quote from the captured source."
    normalized = " ".join(quote.split())
    return {
        "schema_version": "1.0.0",
        "source_system": "tinlance-web-intelligence",
        "tenant_ref": tenant_ref,
        "source_job_id": source_job_id,
        "claim_id": "postgres-intake-test",
        "statement": "A candidate source-backed statement.",
        "source_url": "https://example.com/source",
        "source_url_redacted": False,
        "retrieved_at": "2026-10-18T12:00:00+00:00",
        "media_type": "text/html",
        "artifact_sha256": hashlib.sha256(b"artifact").hexdigest(),
        "quote": quote,
        "quote_sha256": hashlib.sha256(normalized.encode()).hexdigest(),
        "verifier_version": "twi-citation-verifier/1.0.0",
        "report_sha256": hashlib.sha256(b"report").hexdigest(),
    }


@unittest.skipUnless(
    os.environ.get("WORLD_INTELLIGENCE_TEST_DATABASE_URL"),
    "PostgreSQL integration test requires WORLD_INTELLIGENCE_TEST_DATABASE_URL",
)
class PostgresTWISourceEvidenceTests(unittest.TestCase):
    def test_postgres_store_is_idempotent_and_rejects_payload_conflicts(self) -> None:
        from psycopg_pool import ConnectionPool

        pool = ConnectionPool(
            os.environ["WORLD_INTELLIGENCE_TEST_DATABASE_URL"],
            min_size=1,
            max_size=2,
            open=True,
        )
        tenant_ref = hashlib.sha256(uuid.uuid4().bytes).hexdigest()
        idempotency_key = "twi-postgres-" + uuid.uuid4().hex
        payload = _payload(tenant_ref, "job-" + uuid.uuid4().hex)
        store = PostgresSourceEvidenceStore(pool)
        try:
            first = store.ingest(
                payload,
                idempotency_key=idempotency_key,
                request_id="postgres-intake-test",
                traceparent=None,
            )
            replay = store.ingest(
                payload,
                idempotency_key=idempotency_key,
                request_id="postgres-intake-replay",
                traceparent=None,
            )
            self.assertFalse(first["replayed"])
            self.assertTrue(replay["replayed"])
            self.assertEqual(first["evidence_id"], replay["evidence_id"])

            changed = dict(payload)
            changed["statement"] = "A different statement."
            with self.assertRaises(IdempotencyConflictError):
                store.ingest(
                    changed,
                    idempotency_key=idempotency_key,
                    request_id="postgres-intake-conflict",
                    traceparent=None,
                )
        finally:
            with pool.connection() as connection:
                connection.execute(
                    "DELETE FROM world_intelligence.external_source_evidence "
                    "WHERE tenant_ref = %s AND idempotency_key = %s",
                    (tenant_ref, idempotency_key),
                )
            pool.close()


if __name__ == "__main__":
    unittest.main()
