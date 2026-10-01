"""Dependency-free telemetry reference model."""
from __future__ import annotations
from dataclasses import dataclass,field
from time import monotonic
from uuid import uuid4

@dataclass
class Counter:
    name:str
    value:int=0
    def add(self,amount:int=1)->None:
        if amount<0: raise ValueError("counter increments must be non-negative")
        self.value+=amount

@dataclass
class Histogram:
    name:str
    values:list[float]=field(default_factory=list)
    def observe(self,value:float)->None:
        if value<0: raise ValueError("histogram values must be non-negative")
        self.values.append(value)
    @property
    def count(self)->int: return len(self.values)

@dataclass(frozen=True,slots=True)
class Span:
    trace_id:str
    span_id:str
    name:str
    attributes:dict[str,str]

class Tracer:
    def start_span(self,name:str,attributes:dict[str,str]|None=None)->tuple[Span,float]:
        return Span(uuid4().hex,uuid4().hex,name,attributes or {}),monotonic()

    def end_span(self,span:Span,started:float)->float:
        return monotonic()-started
