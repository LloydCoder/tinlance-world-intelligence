"""Deterministic evidence-quality validation."""
from __future__ import annotations
from datetime import datetime, timezone
from packages.contracts.evidence import QualityIssue, QualityReport

def validate_evidence(*, source_id: str, artifact_id: str, observation_id: str, observed_at: datetime | None,
                      provenance_id: str | None, object_value: object, now: datetime | None = None) -> QualityReport:
    issues: list[QualityIssue] = []
    if not source_id.strip():
        issues.append(QualityIssue("missing_source", "error", "source identity is required"))
    if not artifact_id.strip():
        issues.append(QualityIssue("missing_artifact", "error", "artifact identity is required"))
    if not observation_id.strip():
        issues.append(QualityIssue("missing_observation", "error", "observation identity is required"))
    if observed_at is None:
        issues.append(QualityIssue("missing_observed_at", "error", "observation time is required"))
    else:
        reference = now or datetime.now(timezone.utc)
        if observed_at.tzinfo is None:
            issues.append(QualityIssue("naive_timestamp", "error", "observed_at must be timezone-aware"))
        elif observed_at > reference:
            issues.append(QualityIssue("future_observation", "warning", "observed_at is later than validation time"))
    if provenance_id is None:
        issues.append(QualityIssue("missing_provenance", "error", "provenance reference is required"))
    if object_value is None:
        issues.append(QualityIssue("null_assertion", "error", "evidence assertion value must not be null"))
    errors = sum(i.severity == "error" for i in issues)
    score = max(0.0, 1.0 - min(1.0, errors * 0.25 + sum(i.severity == "warning" for i in issues) * 0.05))
    return QualityReport(valid=errors == 0, score=score, issues=tuple(issues))
