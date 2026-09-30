"""Acquisition boundary. Connectors return contracts and never write intelligence."""
from __future__ import annotations
from abc import ABC, abstractmethod
from packages.contracts import AcquisitionRequest, AcquisitionResponse

class AcquisitionError(RuntimeError):
    """Expected acquisition failure."""

class AcquisitionClient(ABC):
    @abstractmethod
    def fetch(self, request: AcquisitionRequest) -> AcquisitionResponse:
        """Fetch one source representation under connector security policy."""
