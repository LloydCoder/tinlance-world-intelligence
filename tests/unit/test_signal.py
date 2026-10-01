import unittest
from services.signal_engine.evaluate import evaluate
from services.signal_engine.explain import explain

class SignalTests(unittest.TestCase):
    def test_equals(self):
        self.assertTrue(evaluate({"op":"equals","field":"status","value":"active"},{"status":"active"}))
    def test_composition(self):
        self.assertTrue(evaluate({"op":"and","conditions":[{"op":"exists","field":"x"},{"op":"not","condition":{"op":"equals","field":"x","value":0}}]},{"x":1}))
    def test_numeric_and_membership(self):
        self.assertTrue(evaluate({"op":"gte","field":"score","value":0.8},{"score":0.9}))
        self.assertTrue(evaluate({"op":"in","field":"kind","values":["event","change"]},{"kind":"change"}))
    def test_explain(self):
        text=explain({"op":"not","condition":{"op":"equals","field":"x","value":1}},{"x":2})
        self.assertIn("not(",text)

if __name__=="__main__":
    unittest.main()
