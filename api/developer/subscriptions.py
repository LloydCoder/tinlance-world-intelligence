"""Validated subscription registry boundary; delivery remains asynchronous infrastructure."""
from __future__ import annotations
from dataclasses import dataclass
from urllib.parse import urlparse
from packages.contracts.developer_api import ApiSubscription, SubscriptionEvent

@dataclass
class SubscriptionRegistry:
    subscriptions: dict[str,ApiSubscription]

    def add(self, subscription: ApiSubscription) -> None:
        parsed=urlparse(subscription.callback_url)
        if parsed.scheme!="https" or not parsed.hostname:
            raise ValueError("subscription callback must use HTTPS")
        if not subscription.tenant_id.strip():
            raise ValueError("tenant_id is required")
        self.subscriptions[subscription.subscription_id]=subscription

    def active_for(self,event:SubscriptionEvent,resource:str) -> tuple[ApiSubscription,...]:
        return tuple(s for s in self.subscriptions.values() if s.active and s.event==event and s.resource==resource)
