import unittest
from datetime import datetime,timezone
from services.reliability.circuit_breaker import CircuitBreaker,CircuitState
from services.reliability.idempotency import derive_key
from services.reliability.lease import acquire

class ReliabilityTests(unittest.TestCase):
    def test_breaker_opens_and_requires_probe(self):
        breaker=CircuitBreaker(2)
        breaker.record_failure(); self.assertEqual(breaker.state,CircuitState.CLOSED)
        breaker.record_failure(); self.assertEqual(breaker.state,CircuitState.OPEN); self.assertFalse(breaker.allow())
        breaker.probe(); self.assertTrue(breaker.allow()); self.assertEqual(breaker.state,CircuitState.HALF_OPEN)
        breaker.record_success(); self.assertEqual(breaker.state,CircuitState.CLOSED)
    def test_idempotency_is_deterministic(self):
        self.assertEqual(derive_key("ingest","s","a"*64),derive_key("ingest","s","a"*64))
        self.assertNotEqual(derive_key("ingest","s","a"*64),derive_key("ingest","s","b"*64))
    def test_lease_is_timezone_aware(self):
        now=datetime(2026,1,1,tzinfo=timezone.utc)
        lease=acquire("j","worker",30,now)
        self.assertEqual(lease.expires_at.year,2026)

if __name__=="__main__": unittest.main()
