# Job Naming Migration - New Identifiable Names

## Overview

All workflow jobs have been renamed with clear, identifiable prefixes to make it easier to identify which workflow and what each job does.

## New Naming Convention

### CI Tests Workflow Jobs
- `ci-backend-lint` - Backend code linting (Ruff)
- `ci-backend-test` - Backend unit tests (Pytest)
- `ci-backend-integration-test` - Backend integration tests (Pytest)
- `ci-test` - **Aggregate job** (verifies all test jobs)

### Security Scan Workflow Jobs
- `security-secret-scan` - Secret scanning (gitleaks)
- `security-dependency-scan` - Dependency scanning (npm audit, safety)
- `security-scan` - **Aggregate job** (verifies all security jobs)

## Old vs New Job IDs

| Old Name | New Name | Notes |
|----------|----------|-------|
| `backend-lint` | `ci-backend-lint` | Added `ci-` prefix |
| `backend-test` | `ci-backend-test` | Added `ci-` prefix |
| `backend-integration-test` | `ci-backend-integration-test` | Added `ci-` prefix |
| `test` | `ci-test` | Added `ci-` prefix |
| `secret-scan` | `security-secret-scan` | Added `security-` prefix |
| `dependency-scan` | `security-dependency-scan` | Added `security-` prefix |
| `security-scan` | `security-scan` | No change (already clear) |

## Benefits

1. **Clear Identification**: Immediately know which workflow a job belongs to
2. **No Ambiguity**: `ci-backend-lint` vs `security-backend-lint` (if we add it later)
3. **Consistent Naming**: All jobs follow the same pattern
4. **Easy Filtering**: Can filter jobs by prefix (`ci-*`, `security-*`)

## Branch Protection Configuration

### `dev` Branch
**Required Checks:**
- `ci-backend-lint`
- `ci-backend-test`
- `ci-test`
- `security-scan`

### `staging` Branch
**Required Checks:**
- `ci-backend-lint`
- `ci-backend-test`
- `ci-backend-integration-test`
- `ci-test`
- `security-scan`

### `main` Branch
**Required Checks:**
- `ci-backend-lint`
- `ci-backend-test`
- `ci-backend-integration-test`
- `ci-test`
- `security-scan`

## Migration Steps

1. ✅ **Workflows Updated**: All job IDs renamed in workflow files
2. ✅ **Branch Protection Script Updated**: Uses new job IDs
3. ✅ **Verification Script Updated**: Checks new job IDs
4. ⏳ **Clear Existing Rules**: Run `./scripts/clear_branch_protection.sh`
5. ⏳ **Recreate Rules**: Run `./scripts/setup_branch_protection.sh`
6. ⏳ **Verify**: Create test PR and verify status checks appear with new names

## Verification

After migration, verify:

```bash
# 1. Check workflows have new job IDs
./scripts/verify_workflow_jobs.sh

# 2. Check branch protection uses new job IDs
grep "CHECKS=" scripts/setup_branch_protection.sh

# 3. Create test PR and verify status checks
# Status checks should appear as:
#   - ci-backend-lint
#   - ci-backend-test
#   - ci-backend-integration-test
#   - ci-test
#   - security-scan
```

## Related Files

- `.github/workflows/tests.yml` - CI Tests workflow
- `.github/workflows/security-scan.yml` - Security Scan workflow
- `scripts/setup_branch_protection.sh` - Branch protection setup
- `scripts/verify_workflow_jobs.sh` - Job verification
- `dev-doc/WORKFLOW_JOB_VERIFICATION.md` - Job verification docs

