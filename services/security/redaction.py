"""Deterministic secret and sensitive-header redaction."""
from __future__ import annotations

SENSITIVE_HEADERS=frozenset({"authorization","cookie","set-cookie","proxy-authorization","x-api-key","x-auth-token"})

def redact_headers(headers: dict[str,str]) -> dict[str,str]:
    return {key: ("[REDACTED]" if key.lower() in SENSITIVE_HEADERS else value) for key,value in headers.items()}
