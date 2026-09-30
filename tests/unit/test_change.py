import unittest
from services.change_engine.classify import classify,significance
from packages.contracts.change import ChangeType
class ChangeTests(unittest.TestCase):
 def test_created(self): self.assertEqual(classify(None,"x"),ChangeType.CREATED)
 def test_source_outage_not_world_change(self): self.assertEqual(classify("x",None,source_available=False),ChangeType.SOURCE_OUTAGE)
 def test_significance(self): self.assertEqual(significance("a","b"),1.0)
