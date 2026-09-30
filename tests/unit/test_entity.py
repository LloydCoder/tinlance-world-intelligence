import unittest
from packages.contracts.entity import *
from services.entity_pipeline.resolver import EntityResolver
class EntityTests(unittest.TestCase):
 def test_exact_identifier_beats_alias(self):
  e=Entity("e1","company","Acme"); i=Identifier("lei","XYZ"); a=EntityAlias("e1","Acme Corporation","acme corporation")
  r=EntityResolver([e],[('e1',i)], [a]); self.assertEqual(r.resolve(i).method,"exact_identifier")
 def test_alias(self):
  e=Entity("e1","company","Acme"); a=EntityAlias("e1","Acme Corporation","acme corporation")
  self.assertEqual(EntityResolver([e],[],[a]).resolve(name=" ACME CORPORATION ").candidate_entity_id,"e1")
