import unittest
from datetime import datetime, timedelta, timezone
from services.temporal_geospatial.query import PointRecord, haversine_meters, query_points, valid_at

class TemporalGeospatialTests(unittest.TestCase):
    def setUp(self):
        self.t0=datetime(2026,1,1,tzinfo=timezone.utc)
    def test_temporal_interval_is_half_open(self):
        r=PointRecord("p",self.t0,self.t0+timedelta(days=1),self.t0)
        self.assertTrue(valid_at(r,self.t0))
        self.assertFalse(valid_at(r,self.t0+timedelta(days=1)))
    def test_haversine_zero_distance(self):
        self.assertAlmostEqual(haversine_meters(0,0,0,0),0,places=6)
    def test_spatial_and_knowledge_cutoffs_compose(self):
        near=PointRecord("near",self.t0,None,self.t0)
        future_known=PointRecord("future",self.t0,None,self.t0+timedelta(days=2))
        rows=query_points([near,future_known],latitude=0,longitude=0,radius_meters=10,world_at=self.t0,known_at_cutoff=self.t0)
        self.assertEqual([r.record_id for r in rows],["near"])

if __name__=="__main__": unittest.main()
