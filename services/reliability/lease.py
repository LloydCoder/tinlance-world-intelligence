"""Lease semantics for at-least-once workers."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timedelta,timezone

@dataclass(frozen=True,slots=True)
class Lease:
    job_id:str
    worker_id:str
    expires_at:datetime

def acquire(job_id:str,worker_id:str,ttl_seconds:int,now:datetime|None=None)->Lease:
    if ttl_seconds<1 or not worker_id.strip(): raise ValueError("invalid lease parameters")
    when=now or datetime.now(timezone.utc)
    if when.tzinfo is None: raise ValueError("now must be timezone-aware")
    return Lease(job_id,worker_id,when+timedelta(seconds=ttl_seconds))
