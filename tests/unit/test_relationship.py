import unittest
from datetime import datetime,timezone
from services.relationship_pipeline.traverse import traverse
from packages.contracts.relationship import Relationship
from services.relationship_pipeline.temporal import active_at
class RelationshipTests(unittest.TestCase):
 def test_traverse(self): self.assertEqual(traverse([("a","owns","b"),("b","owns","c")],"a",2),{"a","b","c"})
 def test_temporal(self):
  r=Relationship("r","a","owns","b",datetime(2026,1,1,tzinfo=timezone.utc))
  self.assertTrue(active_at(r,datetime(2026,2,1,tzinfo=timezone.utc)))
