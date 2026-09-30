from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class QueryPage: items:list[dict]; next_cursor:str|None; total:int|None
@dataclass(frozen=True,slots=True)
class QueryContext: world_at:str|None=None; known_at:str|None=None; start_at:str|None=None; end_at:str|None=None; lat:float|None=None; lon:float|None=None; radius_meters:float|None=None
