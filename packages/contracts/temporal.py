from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
class AssertionStatus(StrEnum): ASSERTED="asserted"; RETRACTED="retracted"
@dataclass(frozen=True,slots=True)
class TemporalAssertion:
 assertion_id:str; subject_ref:str; predicate:str; object_value:object; valid_from:datetime; valid_to:datetime|None; observed_at:datetime; known_at:datetime; status:AssertionStatus; provenance_id:str|None=None
@dataclass(frozen=True,slots=True)
class WorldSnapshot:
 snapshot_id:str; generated_at:datetime; world_cutoff:datetime; knowledge_cutoff:datetime; ontology_version:str; pipeline_version:str
