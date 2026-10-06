# Security Policy

## Scope

This policy covers security issues in Tinlance World Intelligence, including:

- acquisition and SSRF boundaries;
- malicious or hostile external content;
- prompt injection and unsafe AI-assisted processing;
- authentication and authorization;
- tenant or data isolation;
- provenance and artifact-integrity controls;
- dependency and software-supply-chain risks;
- API abuse, rate limiting, and resource exhaustion;
- secret handling and sensitive-data exposure;
- database migrations and operational boundaries.

## Reporting a vulnerability

> [!WARNING]
> Do not disclose an unpatched vulnerability in a public issue, pull request, discussion, or social post.

Use GitHub's private vulnerability reporting mechanism when it is enabled for the repository. If it is unavailable, send the report to **hello@tinlance.com** with the subject line `Security report — Tinlance World Intelligence`.

Include, where safe:

- affected version or commit;
- concise vulnerability description;
- security impact;
- reproduction steps or a minimal proof of concept;
- affected endpoint, file, or component;
- suggested mitigation, if known.

Do not include live credentials, private customer data, or unnecessary personal information.

## Response targets

These are maintainer response targets, not guarantees:

| Stage | Target |
| --- | --- |
| Initial acknowledgement | Within 3 business days |
| Initial triage | Within 7 business days |
| Severity and remediation plan | Within 14 business days for confirmed issues |
| Critical/high remediation target | As soon as practical; normally within 30 days |
| Coordinated disclosure | Agreed with the reporter after a fix or mitigation is available |

Complex vulnerabilities, upstream dependencies, or coordinated disclosures may require a different timeline.

## Severity guidance

- **Critical:** likely repository, production, credential, or sensitive-data compromise with little user interaction.
- **High:** significant unauthorized access, remote code execution, serious SSRF, or integrity bypass.
- **Medium:** meaningful confidentiality, integrity, availability, or authorization weakness requiring additional conditions.
- **Low:** limited impact or defense-in-depth issue.

## Security engineering principles

- Treat external content as untrusted data.
- Revalidate DNS/IP targets at connection time and after redirects.
- Isolate parsing and acquisition from privileged infrastructure.
- Treat prompt-injection text as data, never instructions.
- Preserve raw artifacts and provenance.
- Fail closed on authorization failures.
- Avoid secrets in logs, fixtures, artifacts, and error messages.
- Bound request size, pagination, retries, and resource consumption.
- Validate externally supplied structured data.
- Test security boundaries with adversarial fixtures.

## Disclosure

Please allow reasonable time for remediation and coordinated disclosure. Credit will be given when requested and appropriate, unless anonymity is preferred.
