"""Conservative multi-source support assessment."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Support:
    evidence_id: str
    source_id: str
    independence_group: str
    weight: float
    contradicts: bool = False

@dataclass(frozen=True, slots=True)
class FusionAssessment:
    support_score: float
    contradiction_score: float
    independent_support_groups: int
    supporting_evidence_ids: tuple[str, ...]
    contradicting_evidence_ids: tuple[str, ...]
    status: str

def assess(supports: list[Support]) -> FusionAssessment:
    groups: dict[str, Support] = {}
    contradictions: list[Support] = []
    for item in supports:
        if not 0 <= item.weight <= 1:
            raise ValueError("weight must be 0..1")
        if item.contradicts:
            contradictions.append(item)
            continue
        existing=groups.get(item.independence_group)
        if existing is None or item.weight > existing.weight:
            groups[item.independence_group]=item
    support_score=min(1.0,sum(item.weight for item in groups.values()))
    contradiction_score=min(1.0,sum(item.weight for item in contradictions))
    if contradiction_score > 0 and support_score > 0:
        status="mixed"
    elif support_score > 0:
        status="supported"
    elif contradiction_score > 0:
        status="contradicted"
    else:
        status="unknown"
    return FusionAssessment(
        support_score, contradiction_score, len(groups),
        tuple(item.evidence_id for item in groups.values()),
        tuple(item.evidence_id for item in contradictions),
        status,
    )
