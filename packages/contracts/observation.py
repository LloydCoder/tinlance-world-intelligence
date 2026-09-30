"""Phase 2 observation contract."""
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Mapping

class ObservationStatus(StrEnum):
    CANDIDATE="candidate"; VALIDATED="validated"; REJECTED="rejected"

@dataclass(frozen=True, slots=True)
class Observation:
    observation_id:str
    artifact_id:str
    source_id:str
    subject_ref:str
    predicate:str
    object_value:Any
    observed_at:datetime
    extracted_at:datetime
    valid_from:datetime|None=None
    valid_to:datetime|None=None
    location:Mapping[str,Any]|None=None
    extraction_method:str="deterministic"
    extraction_version:str="1"
    status:ObservationStatus=ObservationStatus.CANDIDATE
    provenance_id:str|None=None
