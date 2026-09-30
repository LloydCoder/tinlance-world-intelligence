import unittest
from services.acquisition.security import UnsafeFetchTarget, validate_fetch_uri

class AcquisitionSecurityTests(unittest.TestCase):
    def test_https_target_allowed(self):
        self.assertEqual(validate_fetch_uri("https://example.com/feed"),"https://example.com/feed")
    def test_credentials_rejected(self):
        with self.assertRaises(UnsafeFetchTarget): validate_fetch_uri("https://user:pass@example.com/feed")
    def test_local_literal_rejected(self):
        for uri in ("http://127.0.0.1/feed","http://10.0.0.2/feed","http://[::1]/feed"):
            with self.assertRaises(UnsafeFetchTarget): validate_fetch_uri(uri)
    def test_unsupported_scheme_rejected(self):
        with self.assertRaises(UnsafeFetchTarget): validate_fetch_uri("file:///etc/passwd")
