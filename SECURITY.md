# Security Policy

## Scope

Security reports for Tinlance World Intelligence should focus on vulnerabilities in the repository, APIs, processing pipelines, provenance controls, acquisition boundaries, authentication/authorization, dependency supply chain, and data isolation.

## Reporting

Do not publish sensitive vulnerability details in a public issue before coordinated remediation. Use the repository owner's configured private security-reporting mechanism where available.

## Security principles

- Treat external content as untrusted.
- Isolate acquisition from privileged application infrastructure.
- Prevent SSRF and unsafe URL fetching.
- Treat prompt-injection content as data, never instructions.
- Preserve provenance and artifact integrity.
- Fail closed on authorization failures.
- Avoid secret exposure in logs and artifacts.
- Validate all externally supplied structured data.
- Test tenant/data isolation where applicable.
