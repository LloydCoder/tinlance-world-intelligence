import unittest
from pathlib import Path
class WorldMonitorTests(unittest.TestCase):
 def test_first_party_surface_contains_required_views(self):
  html=Path("apps/world-monitor/index.html").read_text()
  for name in ("map","events","entities","timeline","changes","signals","evidence","provenance"): self.assertIn('id="'+name+'"',html)
 def test_app_exists(self): self.assertTrue(Path("apps/world-monitor/app.js").exists())
