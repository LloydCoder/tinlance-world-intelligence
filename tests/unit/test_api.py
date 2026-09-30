import unittest
from api.query.service import IntelligenceQueryService
from api.http.router import IntelligenceRouter
class ApiTests(unittest.TestCase):
 def test_page(self):
  r=IntelligenceRouter(IntelligenceQueryService({"entities":[{"id":"1"},{"id":"2"}]})).dispatch("/v1/entities",1)
  self.assertEqual(r.items,[{"id":"1"}]); self.assertEqual(r.next_cursor,"1")
