"""Bounded local rate limiter; production deployments should use a shared gateway."""
from __future__ import annotations
from collections import defaultdict
from time import monotonic

class FixedWindowLimiter:
    def __init__(self,limit:int=120,window_seconds:float=60.0):
        if limit<1 or window_seconds<=0: raise ValueError("invalid rate limit")
        self.limit=limit; self.window_seconds=window_seconds
        self._windows=defaultdict(lambda:[0,0.0])
    def allow(self,key:str)->bool:
        now=monotonic(); count,started=self._windows[key]
        if now-started>=self.window_seconds:
            count=0; started=now
        if count>=self.limit:
            self._windows[key]=[count,started]; return False
        self._windows[key]=[count+1,started]; return True
