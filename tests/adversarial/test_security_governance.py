import ipaddress
import unittest
from packages.contracts.ecosystem import Capability
from services.security.audit import build_audit_event
from services.security.authz import Principal, authorize
from services.security.fetch_policy import UnsafeFetchTarget, validate_target
from services.security.redaction import redact_headers

class SecurityGovernanceTests(unittest.TestCase):
    def resolver(self,host,port,**kwargs):
        return [(None,None,None,None,("10.0.0.8",port))]
    def public_resolver(self,host,port,**kwargs):
        return [(None,None,None,None,("93.184.216.34",port))]
    def test_private_dns_result_is_rejected(self):
        with self.assertRaises(UnsafeFetchTarget):
            validate_target("https://example.com",resolver=self.resolver)
    def test_public_dns_result_is_allowed(self):
        self.assertEqual(validate_target("https://example.com",resolver=self.public_resolver),("93.184.216.34",))
    def test_tenant_and_purpose_are_required(self):
        principal=Principal("u","tenant-a",frozenset({Capability.QUERY_ENTITY}),frozenset({"analysis"}))
        self.assertTrue(authorize(principal,tenant_id="tenant-a",capability=Capability.QUERY_ENTITY,purpose="analysis"))
        self.assertFalse(authorize(principal,tenant_id="tenant-b",capability=Capability.QUERY_ENTITY,purpose="analysis"))
        self.assertFalse(authorize(principal,tenant_id="tenant-a",capability=Capability.QUERY_ENTITY,purpose="other"))
    def test_sensitive_headers_are_redacted(self):
        result=redact_headers({"Authorization":"Bearer secret","X-API-Key":"key","Accept":"application/json"})
        self.assertEqual(result["Authorization"],"[REDACTED]"); self.assertEqual(result["Accept"],"application/json")
    def test_audit_metadata_is_sanitized(self):
        event=build_audit_event("e","u","t","read","denied",{"token":"secret","headers":{"Cookie":"sid=secret"}})
        self.assertEqual(event.metadata["token"],"[REDACTED]")
        self.assertEqual(event.metadata["headers"]["Cookie"],"[REDACTED]")

if __name__=="__main__": unittest.main()
