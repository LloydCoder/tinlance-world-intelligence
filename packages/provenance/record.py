from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True,slots=True)
class ProvenanceRecord:
 provenance_id:str; entity_id:str; activity_id:str; agent_id:str; generated_at:datetime; used_artifact_id:str; derived_from_id:str|None=None
