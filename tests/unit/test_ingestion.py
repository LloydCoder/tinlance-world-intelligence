import unittest
from datetime import datetime, timezone
from packages.contracts import AcquisitionRequest, AcquisitionResponse
from services.acquisition.interface import AcquisitionClient, AcquisitionError
from services.artifact_ingestion.ledger import InMemoryArtifactLedger
from services.ingestion.coordinator import IngestionCoordinator
from services.acquisition.security import UnsafeFetchTarget
from services.ingestion.queue import InMemoryIngestionQueue, IngestionJob, QueueFull
from services.ingestion.retry import RetryPolicy

class Client(AcquisitionClient):
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = 0
    def fetch(self, request):
        self.calls += 1
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

class IngestionTests(unittest.TestCase):
    def test_retry_policy_is_bounded(self):
        policy = RetryPolicy(max_attempts=3, base_delay_seconds=2, max_delay_seconds=5)
        self.assertEqual(policy.delay_for(0), 2)
        self.assertEqual(policy.delay_for(2), 5)
        self.assertFalse(policy.can_retry(2))
    def test_queue_is_bounded(self):
        q = InMemoryIngestionQueue(maxsize=1)
        req = AcquisitionRequest("s1", "https://example.com")
        q.put(IngestionJob("j1", req))
        with self.assertRaises(QueueFull):
            q.put(IngestionJob("j2", req))
    def test_ingestion_persists_hash_addressed_artifact(self):
        now = datetime.now(timezone.utc)
        response = AcquisitionResponse(200, "text/plain", b"hello", "e1", None, now, "https://example.com", {})
        client = Client([response])
        ledger = InMemoryArtifactLedger()
        result = IngestionCoordinator(client, ledger).ingest(AcquisitionRequest("s1", "https://example.com"))
        self.assertEqual(result.status, "stored")
        self.assertEqual(result.artifact.storage_uri, "sha256://2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824")
        self.assertEqual(len(ledger), 1)
    def test_retry_exhaustion_is_explicit(self):
        client = Client([AcquisitionError("timeout"), AcquisitionError("timeout"), AcquisitionError("timeout")])
        result = IngestionCoordinator(client, InMemoryArtifactLedger()).ingest(AcquisitionRequest("s1", "https://example.com"))
        self.assertEqual(result.status, "failed")
        self.assertEqual(result.attempts, 3)
    def test_private_redirect_target_is_rejected(self):
        now = datetime.now(timezone.utc)
        response = AcquisitionResponse(200, "text/plain", b"hello", "e1", None, now, "http://127.0.0.1", {})
        with self.assertRaises(UnsafeFetchTarget):
            IngestionCoordinator(Client([response]), InMemoryArtifactLedger()).ingest(AcquisitionRequest("s1", "https://example.com"))

    def test_not_modified_does_not_create_artifact(self):
        now = datetime.now(timezone.utc)
        response = AcquisitionResponse(304, None, None, "e1", None, now, "https://example.com", {})
        ledger = InMemoryArtifactLedger()
        result = IngestionCoordinator(Client([response]), ledger).ingest(AcquisitionRequest("s1", "https://example.com", etag="e1"))
        self.assertEqual(result.status, "not_modified")
        self.assertEqual(len(ledger), 0)

if __name__ == "__main__":
    unittest.main()
