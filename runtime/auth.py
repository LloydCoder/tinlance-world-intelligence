"""Fail-closed bearer authentication for the runtime HTTP boundary."""
from __future__ import annotations
import hmac

def authorized(header: str | None, expected: str | None, *, required: bool) -> bool:
    if not required:
        return True
    if not header or not expected:
        return False
    scheme, _, value = header.partition(" ")
    return scheme.lower() == "bearer" and bool(value) and hmac.compare_digest(value, expected)
