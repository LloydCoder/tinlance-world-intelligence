"""Conservative entity-match decisioning with explicit review state."""
from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum

class MatchDecision(StrEnum):
    AUTO_ACCEPT="auto_accept"
    REVIEW="review"
    REJECT="reject"

@dataclass(frozen=True, slots=True)
class MatchCandidate:
    left_entity_id: str
    right_entity_id: str
    score: float
    reasons: tuple[str, ...]

def decide(candidate: MatchCandidate, *, auto_threshold: float = 0.98, review_threshold: float = 0.75) -> MatchDecision:
    if not 0 <= review_threshold <= auto_threshold <= 1:
        raise ValueError("thresholds must satisfy 0 <= review <= auto <= 1")
    if not 0 <= candidate.score <= 1:
        raise ValueError("score must be 0..1")
    if candidate.left_entity_id == candidate.right_entity_id:
        return MatchDecision.REJECT
    if candidate.score >= auto_threshold and candidate.reasons:
        return MatchDecision.AUTO_ACCEPT
    if candidate.score >= review_threshold:
        return MatchDecision.REVIEW
    return MatchDecision.REJECT
