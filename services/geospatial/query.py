from packages.contracts.geospatial import SpatialTemporalQuery
def validate_query(q:SpatialTemporalQuery)->SpatialTemporalQuery:
 if q.radius_meters is not None and q.radius_meters<0: raise ValueError("radius must be non-negative")
 if q.start_at and q.end_at and q.start_at>q.end_at: raise ValueError("time window inverted")
 return q
