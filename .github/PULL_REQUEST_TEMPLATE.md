## Summary

Describe the problem, intended outcome, and scope.

## Architectural impact

- [ ] Provenance preserved
- [ ] Temporal semantics preserved
- [ ] Unknown/contradictory states remain representable
- [ ] External input remains untrusted
- [ ] Ecosystem boundaries remain intact

## Security and privacy

Describe trust-boundary, authorization, SSRF, data-isolation, dependency, or secret-handling implications. Write “None” when not applicable.

## Testing

List the commands and CI checks run.

```text
python -m compileall packages services api tests
python -m unittest discover -s tests -v
python scripts/enterprise_audit.py
python scripts/security_baseline.py
```

## Documentation

- [ ] README updated if user-facing behavior changed
- [ ] Relevant docs updated
- [ ] Changelog updated when appropriate

## Migration / compatibility

Describe schema, API, contract, or deployment migration requirements. Write “None” when not applicable.

## Follow-up work

List known limitations or follow-up issues.

## Checklist

- [ ] No secrets or private data are included
- [ ] The change is focused and reviewable
- [ ] Tests cover the changed behavior
- [ ] CI is expected to pass
