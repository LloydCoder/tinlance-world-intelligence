from dataclasses import dataclass
from urllib.parse import urlparse
from api.query.service import IntelligenceQueryService
@dataclass
class Route:
 method:str; path:str; resource:str
class IntelligenceRouter:
 def __init__(self,service:IntelligenceQueryService):
  self.service=service
  self.routes=tuple(Route("GET",f"/v1/{r}",r) for r in ("entities","events","world-state","changes","signals","evidence","provenance"))
 def dispatch(self,path:str,limit:int=100):
  p=urlparse(path).path
  for route in self.routes:
   if p==route.path: return self.service.query(route.resource,limit=limit)
  raise KeyError(path)
