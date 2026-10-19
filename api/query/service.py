"""In-memory query service with fail-closed tenant/capability/purpose policy."""
from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone

from packages.contracts.api import QueryContext, QueryPage
from packages.contracts.ecosystem import Capability

RESOURCE_CAPABILITIES = {
    "entities": Capability.QUERY_ENTITY.value,
    "events": Capability.QUERY_EVENT.value,
    "world-state": Capability.QUERY_WORLD_STATE.value,
    "changes": Capability.QUERY_CHANGES.value,
    "signals": Capability.QUERY_SIGNALS.value,
    "evidence": Capability.QUERY_EVIDENCE.value,
    "provenance": Capability.QUERY_PROVENANCE.value,
}

class IntelligenceQueryService:
    def __init__(
        self,
        stores: dict[str, list[dict]],
        tenant_policies: dict[str, dict] | None = None,
    ):
        self.stores = stores
        self.tenant_policies = tenant_policies or {}
        self.audit_events: list[dict] = []

    def query(
        self,
        resource: str,
        context: QueryContext | None = None,
        cursor: int = 0,
        limit: int = 100,
    ) -> QueryPage:
        if resource not in self.stores:
            raise KeyError(resource)
        if limit < 1 or limit > 1000 or cursor < 0:
            raise ValueError("invalid pagination")
        capability = RESOURCE_CAPABILITIES.get(resource)
        if capability is None:
            raise KeyError(resource)
        if context is None or not context.tenant_id or not context.subject_id or not context.purpose:
            raise PermissionError("query context required")
        policy = self.tenant_policies.get(context.tenant_id)
        allowed = bool(
            policy
            and capability in policy.get("allowed_capabilities", [])
            and context.purpose in policy.get("allowed_purposes", [])
        )
        self.audit_events.append({
            "actor_id": context.subject_id,
            "tenant_id": context.tenant_id,
            "action": f"query:{resource}",
            "outcome": "allowed" if allowed else "denied",
            "occurred_at": datetime.now(timezone.utc).isoformat(),
            "request_id": context.request_id,
            "traceparent": context.traceparent,
        })
        if not allowed:
            raise PermissionError("tenant policy denied query")
        rows = self.stores[resource]
        # Rows carrying explicit tenant/subject ownership are never shared across scopes.
        rows = [
            row for row in rows
            if ("tenant_id" not in row or row.get("tenant_id") == context.tenant_id)
            and ("subject_id" not in row or row.get("subject_id") == context.subject_id)
        ]
        end = min(cursor + limit, len(rows))
        return QueryPage(rows[cursor:end], str(end) if end < len(rows) else None, len(rows))
