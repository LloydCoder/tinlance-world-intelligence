# Phase 23 — Security, Privacy & Governance

Phase 23 hardens the trust boundaries around acquisition, tenant access, and security telemetry.

## Implemented
- connection-time DNS/IP validation hooks for acquisition targets;
- private, loopback, link-local, multicast, reserved, and unspecified address rejection;
- optional host allowlisting;
- rejection of URL userinfo and fragments;
- fail-closed tenant/capability/purpose authorization;
- deterministic sensitive-header and secret redaction;
- sanitized security audit-event contract;
- append-only security audit schema;
- tenant policy persistence with explicit capability, purpose, and retention fields.

## Security semantics
URL string validation alone is insufficient for SSRF defense. The acquisition client must apply target validation at connection time and revalidate each redirect target. DNS results are treated as security-sensitive and a hostname resolving to any non-public address is rejected by the reference policy.

Authorization is resource-oriented: network location is not authority. Tenant, capability, purpose, and active principal state must all satisfy the policy.

Security logs are evidence for accountability but must not become a secondary secret store. Sensitive values are redacted before audit serialization.

These controls are aligned with OWASP SSRF and logging guidance and NIST zero-trust principles. They are foundational controls; production identity providers, KMS/secret managers, network egress policy, WAF/API gateway, and compliance programs remain deployment concerns.
