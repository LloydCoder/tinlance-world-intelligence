"""Typed read-only SDK facade for Platform-governed World Intelligence queries."""
from packages.contracts.ecosystem import Capability,IntelligenceCapabilityRequest,IntelligenceCapabilityResult

class WorldIntelligenceSDK:
    """Read-only SDK facade preserving Agent Platform as the authority boundary."""
    def __init__(self, requester):
        self._requester = requester

    def _query(
        self,
        capability: Capability,
        tenant_id: str,
        subject: str | None = None,
        purpose: str = "sdk",
        policy_context: str | None = None,
    ) -> IntelligenceCapabilityResult:
        if not tenant_id or tenant_id != tenant_id.strip():
            raise ValueError("tenant_id must be normalized and non-empty")
        if subject is not None and (not subject or subject != subject.strip()):
            raise ValueError("subject must be normalized when supplied")
        if not purpose or purpose != purpose.strip():
            raise ValueError("purpose must be normalized and non-empty")
        if policy_context is not None and policy_context != policy_context.strip():
            raise ValueError("policy_context must be normalized when supplied")
        request = IntelligenceCapabilityRequest(capability, tenant_id, subject, purpose, policy_context)
        return self._requester(request)

    def query_entity(self, tenant_id: str, subject: str, *, purpose: str = "sdk", policy_context: str | None = None) -> IntelligenceCapabilityResult:
        return self._query(Capability.QUERY_ENTITY, tenant_id, subject, purpose, policy_context)

    def query_event(self, tenant_id: str, subject: str, *, purpose: str = "sdk", policy_context: str | None = None) -> IntelligenceCapabilityResult:
        return self._query(Capability.QUERY_EVENT, tenant_id, subject, purpose, policy_context)

    def query_world_state(self, tenant_id: str, subject: str, known_at: str | None = None, *, purpose: str = "sdk", policy_context: str | None = None) -> IntelligenceCapabilityResult:
        return self._query(Capability.QUERY_WORLD_STATE, tenant_id, subject, purpose, policy_context if policy_context is not None else known_at)

    def query_changes(self, tenant_id: str, subject: str | None = None, *, purpose: str = "sdk", policy_context: str | None = None) -> IntelligenceCapabilityResult:
        return self._query(Capability.QUERY_CHANGES, tenant_id, subject, purpose, policy_context)

    def query_signals(self, tenant_id: str, subject: str | None = None, *, purpose: str = "sdk", policy_context: str | None = None) -> IntelligenceCapabilityResult:
        return self._query(Capability.QUERY_SIGNALS, tenant_id, subject, purpose, policy_context)

    def query_evidence(self, tenant_id: str, subject: str | None = None, *, purpose: str = "sdk", policy_context: str | None = None) -> IntelligenceCapabilityResult:
        return self._query(Capability.QUERY_EVIDENCE, tenant_id, subject, purpose, policy_context)

    def query_provenance(self, tenant_id: str, subject: str | None = None, *, purpose: str = "sdk", policy_context: str | None = None) -> IntelligenceCapabilityResult:
        return self._query(Capability.QUERY_PROVENANCE, tenant_id, subject, purpose, policy_context)

    def query_region(self, tenant_id: str, subject: str | None = None, *, purpose: str = "sdk", policy_context: str | None = None) -> IntelligenceCapabilityResult:
        return self._query(Capability.QUERY_REGION, tenant_id, subject, purpose, policy_context)
