"""Artifact ingestion primitives."""
from .ledger import ArtifactCandidate, InMemoryArtifactLedger, build_candidate
__all__=["ArtifactCandidate","InMemoryArtifactLedger","build_candidate"]
