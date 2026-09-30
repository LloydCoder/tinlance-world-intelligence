import unittest
from packages.contracts.ecosystem import Capability,IntelligenceCapabilityRequest
from integrations.agent_os.capabilities import is_read_only
from integrations.agent_platform.governance import authorize
class EcosystemTests(unittest.TestCase):
 def test_capabilities_are_read_only(self): self.assertTrue(all(is_read_only(c) for c in Capability))
 def test_governance_is_explicit(self):
  r=authorize(IntelligenceCapabilityRequest(Capability.QUERY_ENTITY,"t","e"),False,"policy denied")
  self.assertFalse(r.allowed); self.assertEqual(r.reason,"policy denied")
