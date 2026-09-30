from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
class RelationshipStatus(StrEnum): ACTIVE="active"; ENDED="ended"; RETRACTED="retracted"
@dataclass(frozen=True,slots=True)
class Relationship:
 relationship_id:str; subject_id:str; predicate:str; object_id:str; valid_from:datetime; valid_to:datetime|None=None; status:RelationshipStatus=RelationshipStatus.ACTIVE; confidence:float=0.0; provenance_id:str|None=None
@dataclass(frozen=True,slots=True)
class RelationshipChange:
 change_id:str; relationship_id:str; change_type:str; detected_at:datetime; before:dict|None; after:dict|None
