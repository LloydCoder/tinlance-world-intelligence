# Phase 22 — Intelligence API & Developer Platform

Phase 22 makes the intelligence API safer to consume as a stable platform.

## Implemented
- tamper-evident opaque pagination cursors;
- developer capability metadata contracts;
- subscription contracts and registry;
- HTTPS-only callback validation at the contract boundary;
- persistent subscription and delivery-attempt schema;
- SDK-facing primitives that preserve the read-only intelligence boundary.

## Semantics
Pagination cursors are opaque and signed; callers must not construct offsets directly. Subscriptions identify a tenant, event type, resource, and callback endpoint. Callback validation is deliberately limited to the contract boundary; DNS rebinding, egress controls, retries, signatures, and delivery isolation belong to the security/reliability phases.

The API remains versioned and read-oriented. It does not grant execution authority.
