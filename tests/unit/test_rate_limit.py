import unittest
from runtime.rate_limit import FixedWindowLimiter

class RateLimitTests(unittest.TestCase):
    def test_limit(self):
        limiter=FixedWindowLimiter(limit=2,window_seconds=60)
        self.assertTrue(limiter.allow("client"))
        self.assertTrue(limiter.allow("client"))
        self.assertFalse(limiter.allow("client"))

if __name__=="__main__": unittest.main()
