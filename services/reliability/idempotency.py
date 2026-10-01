"""Deterministic idempotency key derivation and conflict detection."""
from __future__ import annotations
from hashlib import sha256

def derive_key(namespace:str,source_id:str,payload_digest:str)->str:
    if not namespace.strip() or not source_id.strip() or len(payload_digest)!=64:
        raise ValueError("invalid idempotency inputs")
    return sha256(f"{namespace}:{source_id}:{payload_digest}".encode()).hexdigest()
