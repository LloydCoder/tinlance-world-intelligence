# Phase 15 — Tinlance Ecosystem

## Boundaries

- **ReconOS** supplies acquisition/recon inputs; World Intelligence canonicalizes them.
- **TADS** consumes canonical entities/events/signals; it does not own world state.
- **Agent OS** consumes bounded intelligence capabilities; it does not receive unrestricted database access.
- **Agent Platform** remains the authority for identity, policy, approval, budgets, execution, and governance.
- **External APIs/SDKs** expose stable read/query contracts with evidence and provenance references.

World Intelligence supplies information and evidence, not authorization. Agent Platform remains
the enforcement authority. All governed capability requests must carry tenant/purpose context and
receive an explicit authorization result before sensitive data is returned.