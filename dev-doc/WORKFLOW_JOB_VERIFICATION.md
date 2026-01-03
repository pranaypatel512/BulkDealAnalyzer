# Workflow Job Verification

## Actual Job IDs in Workflows

### Security Scan Workflow (`.github/workflows/security-scan.yml`)

| Job ID | Display Name | Type | Status |
|--------|--------------|------|--------|
| `secret-scan` | Secret Scan | Individual | ✅ Active |
| `dependency-scan` | Dependency Scan | Individual | ✅ Active |
| `security-scan` | Security Scan | Aggregate | ✅ Active |

**Aggregate Job Logic:**
- `security-scan` depends on: `secret-scan`, `dependency-scan`
- Requires: `secret-scan` must succeed
- Allows: `dependency-scan` can be skipped (no dependencies found)

### Tests Workflow (`.github/workflows/tests.yml`)

| Job ID | Display Name | Type | Status |
|--------|--------------|------|--------|
| `backend-lint` | Backend Lint | Individual | ✅ Active |
| `backend-test` | Backend Tests | Individual | ✅ Active |
| `backend-integration-test` | Backend Integration Tests | Individual | ✅ Active |
| `frontend-lint` | Frontend Lint | Individual | ⏸️ Disabled (`if: false`) |
| `frontend-test` | Frontend Tests | Individual | ⏸️ Disabled (`if: false`) |
| `frontend-build` | Frontend Build | Individual | ⏸️ Disabled (`if: false`) |
| `test` | Test | Aggregate | ✅ Active |

**Aggregate Job Logic:**
- `test` depends on: `backend-lint`, `backend-test`, `backend-integration-test`
- Requires: `backend-lint` and `backend-test` must succeed
- Allows: `backend-integration-test` can be skipped (no integration tests found)

## Branch Protection Strategy

### Option 1: Require Only Aggregate Jobs (Recommended)
**Pros:**
- Simpler configuration
- Avoids duplicate requirements
- Aggregate jobs handle dependency logic

**Cons:**
- Less granular control
- Can't require integration tests separately for staging/main

**Configuration:**
- `dev`: `test`, `security-scan`
- `staging`: `test`, `security-scan`
- `main`: `test`, `security-scan`

### Option 2: Require Individual + Aggregate Jobs (Current)
**Pros:**
- Explicit requirements for each job
- Can require integration tests for staging/main only

**Cons:**
- Duplicate requirements (individual jobs are already checked by aggregate)
- More complex configuration
- Potential for "waiting" state if aggregate job waits for dependencies

**Current Configuration:**
- `dev`: `backend-lint`, `backend-test`, `test`, `security-scan`
- `staging`: `backend-lint`, `backend-test`, `backend-integration-test`, `test`, `security-scan`
- `main`: `backend-lint`, `backend-test`, `backend-integration-test`, `test`, `security-scan`

### Option 3: Require Individual Jobs Only (Not Recommended)
**Pros:**
- Most granular control

**Cons:**
- No aggregate status check
- More complex to manage
- Doesn't leverage aggregate job logic

## Recommended Configuration

**For `dev` branch:**
- `backend-lint` (required)
- `backend-test` (required)
- `test` (aggregate - verifies all test jobs)
- `security-scan` (aggregate - verifies all security jobs)

**For `staging` branch:**
- `backend-lint` (required)
- `backend-test` (required)
- `backend-integration-test` (required - explicit for staging)
- `test` (aggregate - verifies all test jobs)
- `security-scan` (aggregate - verifies all security jobs)

**For `main` branch:**
- `backend-lint` (required)
- `backend-test` (required)
- `backend-integration-test` (required - explicit for main)
- `test` (aggregate - verifies all test jobs)
- `security-scan` (aggregate - verifies all security jobs)

## Verification Commands

```bash
# List all job IDs
grep -E "^  [a-z-]+:" .github/workflows/*.yml | grep -v "^  on:" | sed 's/:$//'

# Verify branch protection script matches
grep -A 1 "CHECKS=" scripts/setup_branch_protection.sh

# Check workflow syntax
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/security-scan.yml'))"
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/tests.yml'))"
```

## Notes

1. **Job IDs vs Display Names:**
   - Branch protection uses **job IDs** (e.g., `backend-lint`)
   - Jobs do NOT have `name` fields to ensure status check contexts match job IDs
   - When a job has a `name` field, GitHub creates status checks as `{workflow} / {name} (event)`
   - Without `name`, status checks use just the job ID, matching branch protection requirements

2. **Aggregate Jobs:**
   - Always use `if: always()` to run even if dependencies fail
   - Check dependency results explicitly
   - Report final status based on dependency results

3. **Disabled Jobs:**
   - `frontend-*` jobs are disabled with `if: false`
   - Don't include in branch protection rules
   - Will be enabled when frontend is ready

