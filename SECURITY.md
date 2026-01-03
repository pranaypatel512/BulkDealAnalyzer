# SECURITY

This file documents required security controls and operational runbooks.

## Policy Highlights

- **Secrets**: Never commit secrets. CI must run secret-scan that fails PRs if secrets detected.
- **Dependencies**: Dependabot or Renovate enabled, Snyk/OSS vulnerability scanning enabled in CI.
- **Admins**: MFA required for admin console access; role-based access control enforced for production systems.

## Runbook: Suspected Secret Leak

1. **Revoke leaked secret** (immediately)
2. **Rotate the secret** across environments and update CI/Secrets store
3. **Create high-priority vulnerability issue** and tag security@
4. **Run full CI security-scan** and audit logs to determine exposure window

## Runtime Protections

- Enforce security headers at middleware:
  - **CSP** (Content Security Policy)
  - **HSTS** (HTTP Strict Transport Security)
  - **X-Frame-Options**
  - **X-Content-Type-Options**
- Rate limiting on public endpoints with sensible defaults and whitelisting for internal services

## DB / RLS

- Enforce Row-Level Security for user-scoped tables
- Add automated tests that run queries with different roles to confirm deny/allow

## CI Checks (Must Be Present)

- **gitleaks/detect-secrets** baseline
- **SAST scanner** (Bandit for Python, ESLint security rules for JS)
- **DAST quick scan** on staging (OWASP ZAP nightly - optional for v1)

## Vulnerability Process

- CVSS score each reported issue
- Assign SLA:
  - **Critical** (24h)
  - **High** (72h)
  - **Medium** (7 days)
  - **Low** (30 days)

## Contact

- security@<company> for incidents and triage

## Minimum Viable Security (Sprint 0)

For solo-dev, these are non-negotiables:

- [x] Secret scanning in CI (gitleaks)
- [x] .env.example only — never real secrets
- [ ] Admin account protected with MFA (when admin module ready)
- [ ] DB Row-Level Security ON from day one (when DB schema ready)
- [ ] Backup strategy written (even if manual)


