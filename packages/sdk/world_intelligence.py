from packages.contracts.ecosystem import Capability,IntelligenceCapabilityRequest,IntelligenceCapabilityResult

class WorldIntelligenceSDK:
    """Read-only SDK facade preserving Agent Platform as the authority boundary."""
    def __init__(self,requester): self._requester=requester
    def _query(self,capability:Capability,tenant_id:str,subject:str|None=None,purpose:str="sdk",policy_context:str|None=None):
        return self._requester(IntelligenceCapabilityRequest(capability,tenant_id,subject,purpose,policy_context))
    def query_entity(self,tenant_id:str,subject:str)->IntelligenceCapabilityResult:
        return self._query(Capability.QUERY_ENTITY,tenant_id,subject)
    def query_event(self,tenant_id:str,subject:str)->IntelligenceCapabilityResult:
        return self._query(Capability.QUERY_EVENT,tenant_id,subject)
    def query_world_state(self,tenant_id:str,subject:str,known_at:str|None=None)->IntelligenceCapabilityResult:
        return self._query(Capability.QUERY_WORLD_STATE,tenant_id,subject,"sdk",known_at)
    def query_changes(self,tenant_id:str,subject:str|None=None)->IntelligenceCapabilityResult:
        return self._query(Capability.QUERY_CHANGES,tenant_id,subject)
    def query_signals(self,tenant_id:str,subject:str|None=None)->IntelligenceCapabilityResult:
        return self._query(Capability.QUERY_SIGNALS,tenant_id,subject)
    def query_evidence(self,tenant_id:str,subject:str|None=None)->IntelligenceCapabilityResult:
        return self._query(Capability.QUERY_EVIDENCE,tenant_id,subject)
    def query_provenance(self,tenant_id:str,subject:str|None=None)->IntelligenceCapabilityResult:
        return self._query(Capability.QUERY_PROVENANCE,tenant_id,subject)
    def query_region(self,tenant_id:str,subject:str|None=None)->IntelligenceCapabilityResult:
        return self._query(Capability.QUERY_REGION,tenant_id,subject)
