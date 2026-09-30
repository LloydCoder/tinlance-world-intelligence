import unittest
from services.source_registry import SourceHealthTracker, SourceRegistry, SourceRegistryError
from packages.contracts import Source, SourceHealthStatus

class SourceRegistryTests(unittest.TestCase):
    def test_uri_is_unique(self):
        registry=SourceRegistry()
        registry.register(Source("one","One","https://example.com/feed","rss"))
        with self.assertRaises(SourceRegistryError):
            registry.register(Source("two","Two","https://example.com/feed","rss"))
    def test_health_degrades_then_becomes_unavailable(self):
        tracker=SourceHealthTracker()
        self.assertEqual(tracker.record_failure("s","timeout",10).status,SourceHealthStatus.DEGRADED)
        tracker.record_failure("s","timeout",10)
        self.assertEqual(tracker.record_failure("s","timeout",10).status,SourceHealthStatus.UNAVAILABLE)
        self.assertEqual(tracker.record_success("s",5).consecutive_failures,0)
