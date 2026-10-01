"""Canonical assertion fingerprints for deterministic evidence identity."""
from __future__ import annotations
import json
from hashlib import sha256

def assertion_fingerprint(subject_ref: str, predicate: str, object_value: object) -> str:
    payload=json.dumps({"subject":subject_ref,"predicate":predicate,"object":object_value},sort_keys=True,separators=(",",":"),ensure_ascii=False)
    return sha256(payload.encode("utf-8")).hexdigest()
