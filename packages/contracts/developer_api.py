"""Developer API contracts for pagination, subscriptions, and capability discovery."""
from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum

class SubscriptionEvent(StrEnum):
    CHANGE="change"
    SIGNAL="signal"
    EVENT="event"

@dataclass(frozen=True, slots=True)
class ApiSubscription:
    subscription_id: str
    tenant_id: str
    event: SubscriptionEvent
    resource: str
    callback_url: str
    active: bool = True

@dataclass(frozen=True, slots=True)
class ApiCapability:
    name: str
    version: str
    description: str
    read_only: bool
