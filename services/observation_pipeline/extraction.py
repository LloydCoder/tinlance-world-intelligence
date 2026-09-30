"""Extraction contracts: extractors produce candidates, never authority."""
from __future__ import annotations
from abc import ABC, abstractmethod
from packages.contracts.observation import Observation

class ExtractionError(RuntimeError): pass

class ObservationExtractor(ABC):
    @property
    @abstractmethod
    def version(self)->str: ...
    @abstractmethod
    def extract(self, artifact_id:str, source_id:str, payload:bytes)->list[Observation]:
        """Return candidates linked to the exact artifact."""
