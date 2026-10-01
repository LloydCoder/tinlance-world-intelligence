"""Bounded in-memory queue reference implementation for ingestion work."""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from packages.contracts import AcquisitionRequest

class QueueFull(RuntimeError):
    pass

@dataclass(frozen=True, slots=True)
class IngestionJob:
    job_id: str
    request: AcquisitionRequest
    attempt: int = 0

class InMemoryIngestionQueue:
    def __init__(self, maxsize: int = 1000) -> None:
        if maxsize < 1:
            raise ValueError("maxsize must be positive")
        self._items: deque[IngestionJob] = deque()
        self._maxsize = maxsize

    def put(self, job: IngestionJob) -> None:
        if len(self._items) >= self._maxsize:
            raise QueueFull("ingestion queue is full")
        self._items.append(job)

    def get(self) -> IngestionJob | None:
        return self._items.popleft() if self._items else None

    def __len__(self) -> int:
        return len(self._items)
