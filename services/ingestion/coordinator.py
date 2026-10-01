"""Acquisition-to-artifact orchestration with explicit failure semantics."""
from __future__ import annotations
from dataclasses import dataclass
from packages.contracts import AcquisitionRequest, AcquisitionResponse, RawArtifact
from services.acquisition.interface import AcquisitionClient, AcquisitionError
from services.artifact_ingestion.ledger import InMemoryArtifactLedger, build_candidate
from services.ingestion.retry import RetryPolicy
from services.acquisition.security import validate_fetch_uri

@dataclass(frozen=True, slots=True)
class IngestionResult:
    status: str
    artifact: RawArtifact | None
    attempts: int
    error: str | None = None

class IngestionCoordinator:
    def __init__(self, client: AcquisitionClient, ledger: InMemoryArtifactLedger, retry: RetryPolicy | None = None):
        self.client = client
        self.ledger = ledger
        self.retry = retry or RetryPolicy()

    def ingest(self, request: AcquisitionRequest) -> IngestionResult:
        attempts = 0
        while True:
            attempts += 1
            try:
                validate_fetch_uri(request.uri)
                response: AcquisitionResponse = self.client.fetch(request)
                validate_fetch_uri(response.final_uri)
                if response.status_code == 304 or response.body is None:
                    return IngestionResult("not_modified", None, attempts)
                if response.status_code < 200 or response.status_code >= 300:
                    raise AcquisitionError(f"upstream status {response.status_code}")
                candidate = build_candidate(response.body, response.retrieved_at)
                self.ledger.put(response.body)
                artifact = RawArtifact(
                    artifact_id=candidate.content_sha256,
                    content_sha256=candidate.content_sha256,
                    size_bytes=candidate.size_bytes,
                    media_type=response.media_type,
                    content_encoding=response.headers.get("content-encoding"),
                    storage_uri=f"sha256://{candidate.content_sha256}",
                    source_id=request.source_id,
                    retrieved_at=response.retrieved_at,
                    etag=response.etag,
                    last_modified=response.last_modified,
                )
                return IngestionResult("stored", artifact, attempts)
            except AcquisitionError as exc:
                if not self.retry.can_retry(attempts - 1):
                    return IngestionResult("failed", None, attempts, str(exc))
