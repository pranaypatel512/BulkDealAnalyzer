# Workflow Naming Guide

## Status Check Context Format

GitHub Actions creates status check contexts based on:
- **Workflow name** (top-level `name` field)
- **Job ID** (the key in `jobs:` section)
- **Job name** (optional `name` field within job)

### When Job Has NO `name` Field

Status check context = **Job ID** (e.g., `backend-lint`)

**Example:**
```yaml
name: CI Tests  # Workflow name (doesn't affect status check)

jobs:
  backend-lint:  # Job ID
    runs-on: ubuntu-latest
    # No 'name' field
    steps: [...]
```

**Status Check Context:** `backend-lint` ✅

### When Job HAS `name` Field

Status check context = **`{workflow_name} / {job_name} (event)`**

**Example:**
```yaml
name: CI Tests

jobs:
  backend-lint:
    name: Backend Lint  # Job name
    runs-on: ubuntu-latest
    steps: [...]
```

**Status Check Context:** `CI Tests / Backend Lint (pull_request)` ❌

## Best Practice for Branch Protection

To ensure status check contexts match job IDs (for branch protection):

1. ✅ **Remove `name` fields from jobs** required in branch protection
2. ✅ **Use lowercase, hyphenated workflow names** (optional, for consistency)
3. ✅ **Use job IDs that match the expected status check context**

## Current Configuration

### Tests Workflow
- **Workflow name:** `CI Tests` (descriptive, for UI)
- **Job IDs:** `backend-lint`, `backend-test`, `backend-integration-test`, `test`
- **Status check contexts:** Job IDs (no `name` fields on jobs) ✅

### Security Scan Workflow
- **Workflow name:** `security-scan` (matches job ID pattern)
- **Job IDs:** `secret-scan`, `dependency-scan`, `security-scan`
- **Status check contexts:** Job IDs (no `name` fields on jobs) ✅

## Why Workflow Name Matters (Sometimes)

In some cases, GitHub may use the workflow name in status check contexts:
- When workflow name matches job ID pattern
- When there's ambiguity
- In certain GitHub UI displays

**Solution:** Use lowercase, hyphenated workflow names that match job ID patterns for consistency.

## Verification

After changes, verify status check contexts:

```bash
# 1. Check workflows don't have 'name' fields on required jobs
./scripts/verify_workflow_jobs.sh

# 2. Create a PR and check status checks
# Status checks should appear as job IDs, not full format

# 3. Check branch protection recognizes them
# Settings → Branches → Edit rule → Required checks
```

## Related Files

- `.github/workflows/tests.yml`
- `.github/workflows/security-scan.yml`
- `scripts/verify_workflow_jobs.sh`
- `dev-doc/WORKFLOW_JOB_VERIFICATION.md`

