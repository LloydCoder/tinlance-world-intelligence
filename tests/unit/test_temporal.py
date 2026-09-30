import unittest
from datetime import datetime,timezone
from packages.contracts.temporal import *
from services.temporal.query import state_as_of
class TemporalTests(unittest.TestCase):
 def test_knowledge_as_of(self):
  w=datetime(2026,1,2,tzinfo=timezone.utc); old=TemporalAssertion("a","e","status","old",datetime(2026,1,1,tzinfo=timezone.utc),None,datetime(2026,1,2,tzinfo=timezone.utc),datetime(2026,1,2,tzinfo=timezone.utc),AssertionStatus.ASSERTED)
  future=TemporalAssertion("b","e","status","new",w,None,w,datetime(2026,2,1,tzinfo=timezone.utc),AssertionStatus.ASSERTED)
  self.assertEqual(state_as_of([old,future],w,datetime(2026,1,31,tzinfo=timezone.utc))[0].object_value,"old")
