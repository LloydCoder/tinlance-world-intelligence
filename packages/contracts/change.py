from dataclasses import dataclass
from enum import StrEnum
from datetime import datetime
class ChangeType(StrEnum): CREATED="created"; REMOVED="removed"; MODIFIED="modified"; MOVED="moved"; RELATIONSHIP_CHANGED="relationship_changed"; SOURCE_CORRECTION="source_correction"; SOURCE_OUTAGE="source_outage"
@dataclass(frozen=True,slots=True)
class Change:
 change_id:str; subject_ref:str; change_type:ChangeType; detected_at:datetime; effective_at:datetime|None; before:object|None; after:object|None; significance:float; evidence_ids:tuple[str,...]; world_change:bool
