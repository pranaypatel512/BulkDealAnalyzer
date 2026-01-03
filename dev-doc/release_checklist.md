# Release Checklist

## Automated Checks (Must Pass)

- [ ] Lint (ruff, ESLint)
- [ ] Unit tests (pytest, Jest)
- [ ] Integration tests
- [ ] Security scans (gitleaks, vulnerability scan)
- [ ] Contract tests (OpenAPI) - if applicable
- [ ] Migration dry-run

## Manual Checks (Required)

- [ ] Product signoff
- [ ] Monitoring dashboards configured and ready
- [ ] Runbook updated
- [ ] On-call notified of scheduled release

## Post-Deploy

- [ ] Run synthetic checks for 30 minutes
- [ ] Monitor error rate and latency
- [ ] If threshold exceeded, follow rollback runbook

## Solo-Dev Simplified Checklist

For solo development:

- [ ] All tests pass
- [ ] No secrets in code (gitleaks passes)
- [ ] Manual testing completed
- [ ] Tag release: `git tag v0.1.0`
- [ ] Deploy to staging first
- [ ] Verify staging works
- [ ] Deploy to production
- [ ] Monitor for 30 minutes


