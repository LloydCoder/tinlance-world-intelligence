import unittest
from datetime import datetime, timezone
from packages.provenance import sha256_bytes, validate_sha256
from services.artifact_ingestion import InMemoryArtifactLedger, build_candidate

class ArtifactTests(unittest.TestCase):
    def test_sha256_is_content_identity(self):
        self.assertEqual(sha256_bytes(b"hello world"),"b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9")
    def test_ledger_deduplicates_identical_bytes(self):
        ledger=InMemoryArtifactLedger()
        self.assertEqual(ledger.put(b"same"),ledger.put(b"same"))
        self.assertEqual(len(ledger),1)
    def test_candidate_requires_aware_timestamp(self):
        with self.assertRaises(ValueError): build_candidate(b"x",datetime(2026,1,1))
        candidate=build_candidate(b"x",datetime.now(timezone.utc))
        self.assertTrue(validate_sha256(candidate.content_sha256))
