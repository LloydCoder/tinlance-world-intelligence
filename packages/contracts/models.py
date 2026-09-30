"""Stable domain contracts for Phase 0-1."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Mapping

class HashAlgorithm(StrEnum):
    SHA256 = "sha256"

class ArtifactStatus(StrEnum):
    STORED = "stored"
    NOT_MODIFIED = "not_modified"
    REJECTED = "rejected"

class SourceHealthStatus(StrEnum):
    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"

@dataclass(frozen=True, slots=True)
class Source:
    id: str
    name: str
    canonical_uri: str
    source_type: str
    enabled: bool = True
    expected_interval_seconds: int | None = None
    license_reference: str | None = None

@dataclass(frozen=True, slots=True)
class AcquisitionRequest:
    source_id: str
    uri: str
    method: str = "GET"
    headers: Mapping[str, str] | None = None
    etag: str | None = None
    last_modified: str | None = None

@dataclass(frozen=True, slots=True)
class AcquisitionResponse:
    status_code: int
    media_type: str | None
    body: bytes | None
    etag: str | None
    last_modified: str | None
    retrieved_at: datetime
    final_uri: str
    headers: Mapping[str, str]

@dataclass(frozen=True, slots=True)
class RawArtifact:
    artifact_id: str
    content_sha256: str
    size_bytes: int
    media_type: str | None
    content_encoding: str | None
    storage_uri: str
    source_id: str
    retrieved_at: datetime
    etag: str | None = None
    last_modified: str | None = None
    acquisition_version: str = "1"

@dataclass(frozen=True, slots=True)
class SourceHealth:
    source_id: str
    status: SourceHealthStatus
    checked_at: datetime
    consecutive_failures: int
    latency_ms: int | None
    last_success_at: datetime | None
    last_failure_at: datetime | None
    last_error_code: str | None = None
