from packages.contracts.ecosystem import Capability,IntelligenceCapabilityRequest,IntelligenceCapabilityResult
class WorldIntelligenceSDK:
 def __init__(self,requester): self._requester=requester
 def query_entity(self,tenant_id:str,subject:str)->IntelligenceCapabilityResult:
  return self._requester(IntelligenceCapabilityRequest(Capability.QUERY_ENTITY,tenant_id,subject,"sdk"))
 def query_event(self,tenant_id:str,subject:str)->IntelligenceCapabilityResult:
  return self._requester(IntelligenceCapabilityRequest(Capability.QUERY_EVENT,tenant_id,subject,"sdk"))
 def query_world_state(self,tenant_id:str,subject:str,known_at:str|None=None)->IntelligenceCapabilityResult:
  return self._requester(IntelligenceCapabilityRequest(Capability.QUERY_WORLD_STATE,tenant_id,subject,"sdk",known_at))
