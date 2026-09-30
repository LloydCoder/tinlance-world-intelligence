"""Source health state transitions."""
from __future__ import annotations
from datetime import datetime, timezone
from packages.contracts import SourceHealth, SourceHealthStatus

class SourceHealthTracker:
    def __init__(self)->None:
        self._state:dict[str,SourceHealth]={}

    def record_success(self, source_id:str, latency_ms:int|None, checked_at:datetime|None=None)->SourceHealth:
        now=checked_at or datetime.now(timezone.utc)
        previous=self._state.get(source_id)
        state=SourceHealth(source_id,SourceHealthStatus.HEALTHY,now,0,latency_ms,now,
                           previous.last_failure_at if previous else None,None)
        self._state[source_id]=state
        return state

    def record_failure(self, source_id:str, error_code:str, latency_ms:int|None,
                       checked_at:datetime|None=None)->SourceHealth:
        now=checked_at or datetime.now(timezone.utc)
        previous=self._state.get(source_id)
        failures=(previous.consecutive_failures if previous else 0)+1
        status=SourceHealthStatus.UNAVAILABLE if failures>=3 else SourceHealthStatus.DEGRADED
        state=SourceHealth(source_id,status,now,failures,latency_ms,
                           previous.last_success_at if previous else None,now,error_code)
        self._state[source_id]=state
        return state

    def get(self, source_id:str)->SourceHealth|None:
        return self._state.get(source_id)
