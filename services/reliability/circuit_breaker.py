"""Small deterministic circuit-breaker state machine."""
from __future__ import annotations
from enum import StrEnum

class CircuitState(StrEnum):
    CLOSED="closed"
    OPEN="open"
    HALF_OPEN="half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold:int=5):
        if failure_threshold<1: raise ValueError("failure_threshold must be positive")
        self.failure_threshold=failure_threshold; self.failures=0; self.state=CircuitState.CLOSED
    def record_success(self)->None:
        self.failures=0; self.state=CircuitState.CLOSED
    def record_failure(self)->None:
        self.failures+=1
        if self.failures>=self.failure_threshold: self.state=CircuitState.OPEN
    def allow(self)->bool:
        return self.state in {CircuitState.CLOSED,CircuitState.HALF_OPEN}
    def probe(self)->None:
        if self.state==CircuitState.OPEN: self.state=CircuitState.HALF_OPEN
