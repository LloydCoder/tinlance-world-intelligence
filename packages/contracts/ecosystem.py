from dataclasses import dataclass
from enum import StrEnum
class Capability(StrEnum):
 QUERY_ENTITY="query_entity"; QUERY_EVENT="query_event"; QUERY_WORLD_STATE="query_world_state"; QUERY_CHANGES="query_changes"; QUERY_SIGNALS="query_signals"; QUERY_EVIDENCE="query_evidence"; QUERY_PROVENANCE="query_provenance"; QUERY_REGION="query_region"
@dataclass(frozen=True,slots=True)
class IntelligenceCapabilityRequest:
 capability:Capability; tenant_id:str; subject:str|None=None; purpose:str|None=None; policy_context:str|None=None
@dataclass(frozen=True,slots=True)
class IntelligenceCapabilityResult:
 request_id:str; allowed:bool; data:dict|list|None; evidence_ids:tuple[str,...]; provenance_ids:tuple[str,...]; reason:str|None=None
