from packages.contracts.ecosystem import IntelligenceCapabilityRequest,IntelligenceCapabilityResult
def authorize(request:IntelligenceCapabilityRequest,allowed:bool,reason:str|None=None)->IntelligenceCapabilityResult:
 return IntelligenceCapabilityResult(request_id=f"{request.tenant_id}:{request.capability}",allowed=allowed,data=None,evidence_ids=(),provenance_ids=(),reason=reason)
