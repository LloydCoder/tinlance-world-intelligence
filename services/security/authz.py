"""Fail-closed tenant and capability authorization."""
from __future__ import annotations
from dataclasses import dataclass
from packages.contracts.ecosystem import Capability

@dataclass(frozen=True, slots=True)
class Principal:
    subject_id: str
    tenant_id: str
    capabilities: frozenset[Capability]
    purposes: frozenset[str]
    active: bool = True

def authorize(principal: Principal, *, tenant_id: str, capability: Capability, purpose: str | None) -> bool:
    if not principal.active or principal.tenant_id != tenant_id:
        return False
    if capability not in principal.capabilities:
        return False
    return bool(purpose and purpose in principal.purposes)
