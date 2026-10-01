"""SLO and error-budget calculations."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class SLO:
    name:str
    target:float
    window_days:int=30
    def __post_init__(self):
        if not 0<self.target<=1: raise ValueError("target must be in (0,1]")
        if self.window_days<1: raise ValueError("window_days must be positive")
    def error_budget(self)->float: return 1-self.target
    def remaining_budget(self,observed_success_rate:float)->float:
        if not 0<=observed_success_rate<=1: raise ValueError("success rate must be 0..1")
        return max(0.0,observed_success_rate-self.target)
