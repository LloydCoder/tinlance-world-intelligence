"""Evidence and data-quality contracts."""
from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum
from datetime import datetime

class EvidenceStatus(StrEnum):
    CANDIDATE="candidate"
    VALIDATED="validated"
    REJECTED="rejected"

@dataclass(frozen=True, slots=True)
class Evidence:
    evidence_id: str
    observation_id: str
    artifact_id: str
    source_id: str
    assertion_fingerprint: str
    status: EvidenceStatus
    quality_score: float
    observed_at: datetime
    provenance_id: str | None = None

@dataclass(frozen=True, slots=True)
class QualityIssue:
    code: str
    severity: str
    message: str

@dataclass(frozen=True, slots=True)
class QualityReport:
    valid: bool
    score: float
    issues: tuple[QualityIssue, ...]
