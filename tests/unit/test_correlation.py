import unittest
from services.correlation.independence import independent_count
from services.correlation.contradiction import contradiction
class CorrelationTests(unittest.TestCase):
 def test_dependency_not_independent(self): self.assertEqual(independent_count("a",{"b","c"},{("b","a")}),1)
 def test_contradiction(self): self.assertTrue(contradiction({"subject_ref":"e","predicate":"x","object_value":1},{"subject_ref":"e","predicate":"x","object_value":2}))
