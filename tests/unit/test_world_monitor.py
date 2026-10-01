import unittest
from pathlib import Path

class WorldMonitorTests(unittest.TestCase):
    def test_first_party_surface_contains_required_views(self):
        html=Path("apps/world-monitor/index.html").read_text()
        for name in ("map","events","entities","timeline","changes","signals","evidence","provenance"):
            self.assertIn('id="'+name+'"',html)
    def test_browser_security_policy_is_present(self):
        html=Path("apps/world-monitor/index.html").read_text()
        self.assertIn("Content-Security-Policy",html)
        self.assertIn("frame-ancestors 'none'",html)
    def test_app_exists_and_avoids_untrusted_innerhtml(self):
        app=Path("apps/world-monitor/app.js").read_text()
        self.assertNotIn("innerHTML",app)
        self.assertIn("demo=1",app)
        self.assertIn("WORLD_INTELLIGENCE_CONFIG",app)
    def test_app_exists(self):
        self.assertTrue(Path("apps/world-monitor/app.js").exists())

if __name__=="__main__": unittest.main()
