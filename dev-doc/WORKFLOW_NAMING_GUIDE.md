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
- **Workflow name:** `Security Scan` (descriptive, doesn't match job IDs)
- **Job IDs:** `security-secret-scan`, `security-dependency-scan`, `security-scan`
- **Status check contexts:** Job IDs (no `name` fields on jobs) ✅

## Why Workflow Name Matters

**IMPORTANT:** When a workflow name exactly matches a job ID, GitHub creates status check contexts as `{workflow_name} / {job_id} (event)` instead of just `{job_id}`.

**Example of the Problem:**
```yaml
name: security-scan  # ❌ Matches job ID

jobs:
  security-scan:  # Same name!
    runs-on: ubuntu-latest
```

**Result:** Status check context = `security-scan / security-scan (pull_request)`  
**Branch Protection Expects:** `security-scan`  
**Outcome:** Status check shows as "waiting" even though job passed ✅

**Solution:** Use descriptive workflow names that **don't match any job ID**:
```yaml
name: Security Scan  # ✅ Descriptive, doesn't match job IDs

jobs:
  security-scan:  # Different from workflow name
    runs-on: ubuntu-latest
```

**Result:** Status check context = `security-scan` (just the job ID) ✅

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

