import unittest
from services.advanced.anomaly import z_score
class AdvancedTests(unittest.TestCase):
 def test_z_score(self): self.assertEqual(z_score(12,10,2),1)
 def test_zero_variance(self): self.assertEqual(z_score(10,10,0),0)
