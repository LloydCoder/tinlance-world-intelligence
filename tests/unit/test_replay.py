import unittest
from services.replay.backtest import backtest
from packages.contracts.replay import ReplayManifest
class ReplayTests(unittest.TestCase):
 def test_backtest_metrics(self):
  r=backtest("r",{"a","b"},{"a","c"},3); self.assertEqual(r.precision,.5); self.assertEqual(r.recall,.5)
