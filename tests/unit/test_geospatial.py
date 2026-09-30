import unittest
from datetime import datetime,timezone
from packages.contracts.geospatial import SpatialTemporalQuery
from services.geospatial.query import validate_query
class GeospatialTests(unittest.TestCase):
 def test_radius(self): self.assertIsNotNone(validate_query(SpatialTemporalQuery(None,radius_meters=10)))
 def test_invalid_window(self):
  a=datetime(2026,2,1,tzinfo=timezone.utc); b=datetime(2026,1,1,tzinfo=timezone.utc)
  with self.assertRaises(ValueError): validate_query(SpatialTemporalQuery(None,a,b))
