from packages.contracts.ecosystem import Capability,IntelligenceCapabilityRequest
class TADSClient:
 def request_signal(self,tenant_id:str,subject:str)->IntelligenceCapabilityRequest:
  return IntelligenceCapabilityRequest(Capability.QUERY_SIGNALS,tenant_id,subject,"tads_target_intelligence")
