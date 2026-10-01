"""Opaque, tamper-evident cursor codec for query pagination."""
from __future__ import annotations
import base64
import hashlib
import hmac
import json

class InvalidCursor(ValueError):
    pass

def encode_cursor(offset: int, *, secret: str) -> str:
    if offset < 0:
        raise ValueError("offset must be non-negative")
    payload=json.dumps({"offset":offset},separators=(",",":"),sort_keys=True).encode()
    signature=hmac.new(secret.encode(),payload,hashlib.sha256).digest()
    return base64.urlsafe_b64encode(payload+b"."+signature).decode().rstrip("=")

def decode_cursor(cursor: str, *, secret: str) -> int:
    try:
        raw=base64.urlsafe_b64decode(cursor+"="*((4-len(cursor)%4)%4))
        payload,signature=raw.rsplit(b".",1)
        expected=hmac.new(secret.encode(),payload,hashlib.sha256).digest()
        if not hmac.compare_digest(signature,expected):
            raise InvalidCursor("invalid cursor signature")
        value=json.loads(payload.decode())
        offset=value["offset"]
        if not isinstance(offset,int) or offset<0:
            raise InvalidCursor("invalid cursor offset")
        return offset
    except (ValueError,KeyError,TypeError,UnicodeError,json.JSONDecodeError) as exc:
        raise InvalidCursor("invalid cursor") from exc
