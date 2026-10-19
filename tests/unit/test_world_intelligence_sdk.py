import unittest

from packages.contracts.ecosystem import Capability, IntelligenceCapabilityResult
from packages.sdk.world_intelligence import WorldIntelligenceSDK

class WorldIntelligenceSDKTests(unittest.TestCase):
    def setUp(self):
        self.requests = []
        self.result = IntelligenceCapabilityResult("request-1", True, {"items": []}, (), ())
        def requester(request):
            self.requests.append(request)
            return self.result
        self.sdk = WorldIntelligenceSDK(requester)

    def test_query_entity_propagates_purpose_and_policy_context(self):
        result = self.sdk.query_entity("tenant-a", "subject-a", purpose="account_research", policy_context="case-17")
        self.assertIs(result, self.result)
        request = self.requests[0]
        self.assertEqual(request.capability, Capability.QUERY_ENTITY)
        self.assertEqual(request.tenant_id, "tenant-a")
        self.assertEqual(request.subject, "subject-a")
        self.assertEqual(request.purpose, "account_research")
        self.assertEqual(request.policy_context, "case-17")

    def test_region_capability_is_exposed_by_sdk(self):
        self.sdk.query_region("tenant-a", purpose="regional_risk")
        self.assertEqual(self.requests[0].capability, Capability.QUERY_REGION)
        self.assertEqual(self.requests[0].purpose, "regional_risk")

    def test_invalid_tenant_and_purpose_fail_closed(self):
        with self.assertRaises(ValueError):
            self.sdk.query_entity(" tenant-a", "subject-a")
        with self.assertRaises(ValueError):
            self.sdk.query_entity("tenant-a", "subject-a", purpose=" ")

if __name__ == "__main__":
    unittest.main()
