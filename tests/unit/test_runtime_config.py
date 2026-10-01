import os
import unittest
from runtime.config import ConfigurationError,RuntimeConfig

class RuntimeConfigTests(unittest.TestCase):
    def test_production_requires_postgres(self):
        old=dict(os.environ)
        try:
            os.environ.update({"WORLD_INTELLIGENCE_ENV":"production","WORLD_INTELLIGENCE_BEARER_TOKEN":"x","WORLD_INTELLIGENCE_STORAGE_MODE":"memory"})
            with self.assertRaises(ConfigurationError):
                RuntimeConfig.from_env()
        finally:
            os.environ.clear(); os.environ.update(old)
    def test_development_allows_memory(self):
        old=dict(os.environ)
        try:
            for key in ("WORLD_INTELLIGENCE_ENV","WORLD_INTELLIGENCE_STORAGE_MODE","DATABASE_URL","WORLD_INTELLIGENCE_BEARER_TOKEN"):
                os.environ.pop(key,None)
            cfg=RuntimeConfig.from_env()
            self.assertEqual(cfg.storage_mode,"memory")
        finally:
            os.environ.clear(); os.environ.update(old)

if __name__=="__main__": unittest.main()
