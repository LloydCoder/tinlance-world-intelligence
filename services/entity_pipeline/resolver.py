from packages.contracts.entity import Identifier,EntityResolution
from .normalize import normalize_identifier,normalize_alias
class EntityResolver:
 def __init__(self,entities=(),identifiers=(),aliases=()):
  self.entities={e.entity_id:e for e in entities}
  self.ids={normalize_identifier(i.value):(i.scheme,i.value,eid) for eid,i in identifiers}
  self.aliases={normalize_alias(a.alias):a.entity_id for a in aliases}
 def resolve(self,identifier:Identifier|None=None,name:str|None=None)->EntityResolution|None:
  if identifier:
   hit=self.ids.get(normalize_identifier(identifier.value))
   if hit: return EntityResolution(hit[2],"exact_identifier",1.0,identifier)
  if name:
   eid=self.aliases.get(normalize_alias(name))
   if eid: return EntityResolution(eid,"exact_alias",0.95,None,name)
  return None
