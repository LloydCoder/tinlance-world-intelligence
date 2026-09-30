import unittest
from datetime import datetime,timezone
from packages.contracts.event import Event,EventStatus
from services.event_pipeline.correlate import correlate
from services.event_pipeline.lifecycle import transition
class EventTests(unittest.TestCase):
 def e(self,i,t="x"): return Event(i,t,i,datetime(2026,1,1,tzinfo=timezone.utc))
 def test_correlation(self): self.assertEqual(len(correlate([self.e("a"),self.e("b")])),1)
 def test_lifecycle(self): self.assertEqual(transition(self.e("a"),EventStatus.CONFIRMED).status,EventStatus.CONFIRMED)
 def test_invalid_transition(self):
  with self.assertRaises(ValueError): transition(self.e("a"),EventStatus.RESOLVED)
