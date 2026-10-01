from dataclasses import dataclass
from urllib.parse import parse_qs,urlparse
from api.query.service import IntelligenceQueryService

@dataclass
class Route:
    method:str
    path:str
    resource:str

class IntelligenceRouter:
    def __init__(self,service):
        self.service=service
        self.routes=tuple(Route("GET",f"/v1/{r}",r) for r in ("entities","events","world-state","changes","signals","evidence","provenance"))

    def dispatch(self,path:str):
        parsed=urlparse(path)
        query=parse_qs(parsed.query,keep_blank_values=False)
        try:
            limit=int(query.get("limit",["100"])[0])
            cursor=int(query.get("cursor",["0"])[0])
        except ValueError as exc:
            raise ValueError("cursor and limit must be integers") from exc
        if cursor<0 or limit<1 or limit>1000:
            raise ValueError("invalid pagination")
        for route in self.routes:
            if parsed.path==route.path:
                return self.service.query(route.resource,cursor=cursor,limit=limit)
        raise KeyError(path)
