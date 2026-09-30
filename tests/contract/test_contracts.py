import unittest
from packages.contracts import AcquisitionRequest, Source
from packages.ontology import EntityType, EventType

class ContractTests(unittest.TestCase):
    def test_contracts_are_framework_free(self):
        source=Source("src-1","Example","https://example.com","web")
        request=AcquisitionRequest(source.id,source.canonical_uri)
        self.assertEqual(request.method,"GET")
        self.assertEqual(EntityType.COMPANY.value,"company")
        self.assertEqual(EventType.GENERIC.value,"generic")
