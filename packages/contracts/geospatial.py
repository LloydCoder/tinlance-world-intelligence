from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True,slots=True)
class SpatialFeature:
 feature_id:str; geometry_geojson:dict; srid:int=4326
@dataclass(frozen=True,slots=True)
class SpatialTemporalQuery:
 geometry_geojson:dict|None; start_at:datetime|None=None; end_at:datetime|None=None; radius_meters:float|None=None
