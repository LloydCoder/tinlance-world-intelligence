"""Deterministic retry policy with bounded exponential backoff."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 60.0

    def delay_for(self, attempt: int) -> float:
        if attempt < 0:
            raise ValueError("attempt must be non-negative")
        return min(self.max_delay_seconds, self.base_delay_seconds * (2 ** attempt))

    def can_retry(self, attempt: int) -> bool:
        return attempt + 1 < self.max_attempts
