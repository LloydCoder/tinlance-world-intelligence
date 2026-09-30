"""Content-addressing primitives."""
from __future__ import annotations
import hashlib
from pathlib import Path

SHA256_HEX_LENGTH=64

def sha256_bytes(data: bytes)->str:
    return hashlib.sha256(data).hexdigest()

def sha256_file(path: str|Path, chunk_size: int=1024*1024)->str:
    digest=hashlib.sha256()
    with Path(path).open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()

def validate_sha256(value: str)->bool:
    if len(value)!=SHA256_HEX_LENGTH: return False
    try: int(value,16)
    except ValueError: return False
    return True
