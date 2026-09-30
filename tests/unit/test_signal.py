import unittest
from services.signal_engine.evaluate import evaluate
from services.signal_engine.explain import explain
class SignalTests(unittest.TestCase):
 def test_equals(self): self.assertTrue(evaluate({"op":"equals","field":"status","value":"open"},{"status":"open"}))
 def test_composition(self):
  rule={"op":"and","conditions":[{"op":"exists","field":"x"},{"op":"equals","field":"x","value":1}]}
  self.assertTrue(evaluate(rule,{"x":1}))
 def test_explain(self): self.assertIn("equals",explain({"op":"equals","field":"x","value":1},{"x":1}))
