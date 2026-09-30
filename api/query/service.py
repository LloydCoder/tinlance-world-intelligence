from packages.contracts.api import QueryPage,QueryContext
class IntelligenceQueryService:
 def __init__(self,stores:dict[str,list[dict]]): self.stores=stores
 def query(self,resource:str,context:QueryContext=QueryContext(),cursor:int=0,limit:int=100)->QueryPage:
  if resource not in self.stores: raise KeyError(resource)
  if limit<1 or limit>1000: raise ValueError("limit must be 1..1000")
  rows=self.stores[resource]; end=min(cursor+limit,len(rows))
  return QueryPage(rows[cursor:end],str(end) if end<len(rows) else None,len(rows))
