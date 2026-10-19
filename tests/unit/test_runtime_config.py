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
    def test_production_requires_source_evidence_service_token(self):
        old = dict(os.environ)
        try:
            os.environ.update({
                "WORLD_INTELLIGENCE_ENV": "production",
                "WORLD_INTELLIGENCE_BEARER_TOKEN": "read-token",
                "WORLD_INTELLIGENCE_STORAGE_MODE": "postgres",
                "DATABASE_URL": "postgresql://example.invalid/db",
            })
            os.environ.pop("WORLD_INTELLIGENCE_SOURCE_EVIDENCE_TOKEN", None)
            with self.assertRaisesRegex(ConfigurationError, "source evidence service token"):
                RuntimeConfig.from_env()
        finally:
            os.environ.clear()
            os.environ.update(old)

    def test_development_allows_memory(self):
        old=dict(os.environ)
        try:
            for key in ("WORLD_INTELLIGENCE_ENV","WORLD_INTELLIGENCE_STORAGE_MODE","DATABASE_URL","WORLD_INTELLIGENCE_BEARER_TOKEN"):
                os.environ.pop(key,None)
            cfg=RuntimeConfig.from_env()
            self.assertEqual(cfg.storage_mode,"memory")
        finally:
            os.environ.clear(); os.environ.update(old)


    def test_production_requires_platform_jwt_configuration(self):
        old = dict(os.environ)
        try:
            os.environ.update({
                "WORLD_INTELLIGENCE_ENV": "production",
                "WORLD_INTELLIGENCE_REQUIRE_AUTH": "true",
                "WORLD_INTELLIGENCE_SOURCE_EVIDENCE_TOKEN": "source-token",
                "WORLD_INTELLIGENCE_STORAGE_MODE": "postgres",
                "DATABASE_URL": "postgresql://example.invalid/db",
            })
            for key in ("WORLD_INTELLIGENCE_PLATFORM_ISSUER", "WORLD_INTELLIGENCE_PLATFORM_AUDIENCE", "WORLD_INTELLIGENCE_PLATFORM_JWKS_URL"):
                os.environ.pop(key, None)
            with self.assertRaisesRegex(ConfigurationError, "Platform issuer, audience, and JWKS URL"):
                RuntimeConfig.from_env()
        finally:
            os.environ.clear()
            os.environ.update(old)

    def test_production_cannot_disable_query_authentication(self):
        old = dict(os.environ)
        try:
            os.environ.update({
                "WORLD_INTELLIGENCE_ENV": "production",
                "WORLD_INTELLIGENCE_REQUIRE_AUTH": "false",
                "WORLD_INTELLIGENCE_SOURCE_EVIDENCE_TOKEN": "source-token",
                "WORLD_INTELLIGENCE_STORAGE_MODE": "postgres",
                "DATABASE_URL": "postgresql://example.invalid/db",
                "WORLD_INTELLIGENCE_PLATFORM_ISSUER": "https://identity.tinlance.test",
                "WORLD_INTELLIGENCE_PLATFORM_AUDIENCE": "world-intelligence",
                "WORLD_INTELLIGENCE_PLATFORM_JWKS_URL": "https://identity.tinlance.test/.well-known/jwks.json",
            })
            with self.assertRaisesRegex(ConfigurationError, "cannot be disabled"):
                RuntimeConfig.from_env()
        finally:
            os.environ.clear()
            os.environ.update(old)


if __name__=="__main__": unittest.main()
