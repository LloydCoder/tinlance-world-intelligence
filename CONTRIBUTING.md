# Contributing

Thank you for contributing to Tinlance World Intelligence.

## Before you start

A contribution should:

1. Belong to the intelligence-fabric boundary.
2. Preserve provenance and source attribution.
3. Keep temporal semantics explicit.
4. Preserve unknown, contradictory, and unavailable states.
5. Treat external content as untrusted.
6. Avoid duplicating ReconOS, TADS, Agent OS, or Agent Platform authority.
7. Include tests for changed behavior.
8. Update documentation when behavior, contracts, security boundaries, or operational procedures change.

For security-sensitive changes, read [SECURITY.md](SECURITY.md) first.

## Development workflow

1. Fork the repository.
2. Clone your fork and enter the repository.
3. Create a focused branch from `main`.
4. Make the smallest coherent change.
5. Run the local verification commands.
6. Update documentation and changelog entries when appropriate.
7. Open a pull request with the required context.

Example:

```bash
git clone https://github.com/YOUR-USER/tinlance-world-intelligence.git
cd tinlance-world-intelligence
git switch -c fix/short-description
python -m compileall packages services api tests
python -m unittest discover -s tests -v
```

## Pull requests

Every PR should explain:

- problem and intended outcome;
- scope and affected components;
- architectural and integration impact;
- data/provenance impact;
- security and privacy impact;
- migration impact, if any;
- tests and verification performed;
- documentation changes;
- known follow-up work.

Keep PRs reviewable. Avoid unrelated refactors.

## Coding standards

- Python: follow the existing formatting and typing conventions; prefer explicit, readable code.
- SQL: keep migrations ordered and deterministic; never rewrite an applied migration.
- APIs and schemas: preserve backward compatibility unless the change explicitly increments the relevant contract/version.
- Security: validate at trust boundaries and fail closed on authorization failures.
- Tests: prefer deterministic tests with clear fixtures and meaningful failure messages.
- Documentation: use relative repository links; state operational limits honestly.

## Commits

Conventional Commits are recommended:

```
feat: add capability
fix: correct boundary behavior
docs: clarify runtime configuration
test: add regression coverage
security: harden acquisition validation
ci: update workflow
```

Keep commits focused and avoid mixing generated files with unrelated source changes.

## Review expectations

Maintainers may request changes when a proposal weakens provenance, uncertainty handling, security isolation, reproducibility, or ecosystem boundaries.

All changes are subject to CI and maintainer review. CODEOWNERS currently assigns repository ownership to `@LloydCoder`.

## Do not commit

Never commit:

- passwords, API keys, tokens, private keys, or credentials;
- real private customer data;
- local `.env` files;
- generated build output unless explicitly required;
- proprietary source material without permission.

See [SECURITY.md](SECURITY.md) for vulnerability reporting.
