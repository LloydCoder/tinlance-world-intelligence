from dataclasses import dataclass
from enum import StrEnum
from datetime import datetime
class EventStatus(StrEnum): PROPOSED="proposed"; CONFIRMED="confirmed"; RESOLVED="resolved"; CANCELLED="cancelled"
@dataclass(frozen=True,slots=True)
class Event:
 event_id:str; event_type:str; title:str; start_at:datetime; end_at:datetime|None=None; status:EventStatus=EventStatus.PROPOSED; confidence:float=0.0; provenance_id:str|None=None
@dataclass(frozen=True,slots=True)
class EventCorrelation:
 correlation_id:str; event_ids:tuple[str,...]; relation:str; confidence:float
