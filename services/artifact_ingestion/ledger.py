"""Raw artifact ledger primitives."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from packages.provenance import sha256_bytes

@dataclass(frozen=True, slots=True)
class ArtifactCandidate:
    content_sha256: str
    size_bytes: int
    retrieved_at: datetime

def build_candidate(body: bytes, retrieved_at: datetime|None=None)->ArtifactCandidate:
    timestamp=retrieved_at or datetime.now(timezone.utc)
    if timestamp.tzinfo is None:
        raise ValueError("retrieved_at must be timezone-aware")
    return ArtifactCandidate(sha256_bytes(body), len(body), timestamp)

class InMemoryArtifactLedger:
    """Reference ledger used for contract tests; production persistence is database-backed."""
    def __init__(self)->None:
        self._artifacts:dict[str,bytes]={}
    def put(self, body:bytes)->str:
        digest=sha256_bytes(body)
        self._artifacts.setdefault(digest,body)
        return digest
    def get(self, content_sha256:str)->bytes|None:
        return self._artifacts.get(content_sha256)
    def __len__(self)->int:
        return len(self._artifacts)
