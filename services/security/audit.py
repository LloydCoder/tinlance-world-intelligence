"""Security audit-event contract with sanitized payloads."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from services.security.redaction import redact_headers

@dataclass(frozen=True, slots=True)
class AuditEvent:
    event_id: str
    actor_id: str
    tenant_id: str
    action: str
    outcome: str
    occurred_at: datetime
    metadata: dict

def sanitize_metadata(metadata: dict) -> dict:
    clean={}
    for key,value in metadata.items():
        if key.lower() in {"password","secret","token","access_token","refresh_token","private_key"}:
            clean[key]="[REDACTED]"
        elif key.lower()=="headers" and isinstance(value,dict):
            clean[key]=redact_headers(value)
        else:
            clean[key]=value
    return clean

def build_audit_event(event_id:str,actor_id:str,tenant_id:str,action:str,outcome:str,metadata:dict,occurred_at:datetime|None=None)->AuditEvent:
    when=occurred_at or datetime.now(timezone.utc)
    if when.tzinfo is None:
        raise ValueError("occurred_at must be timezone-aware")
    return AuditEvent(event_id,actor_id,tenant_id,action,outcome,when,sanitize_metadata(metadata))
