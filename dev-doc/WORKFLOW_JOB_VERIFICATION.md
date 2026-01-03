# Workflow Job Verification

## Actual Job IDs in Workflows

### Security Scan Workflow (`.github/workflows/security-scan.yml`)

| Job ID | Type | Status |
|--------|------|--------|
| `security-secret-scan` | Individual | ✅ Active |
| `security-dependency-scan` | Individual | ✅ Active |
| `security-scan` | Aggregate | ✅ Active |

**Aggregate Job Logic:**
- `security-scan` depends on: `security-secret-scan`, `security-dependency-scan`
- Requires: `security-secret-scan` must succeed
- Allows: `security-dependency-scan` can be skipped (no dependencies found)

### Tests Workflow (`.github/workflows/tests.yml`)

| Job ID | Type | Status |
|--------|------|--------|
| `ci-backend-lint` | Individual | ✅ Active |
| `ci-backend-test` | Individual | ✅ Active |
| `ci-backend-integration-test` | Individual | ✅ Active |
| `frontend-lint` | Individual | ⏸️ Disabled (`if: false`) |
| `frontend-test` | Individual | ⏸️ Disabled (`if: false`) |
| `frontend-build` | Individual | ⏸️ Disabled (`if: false`) |
| `ci-test` | Aggregate | ✅ Active |

**Aggregate Job Logic:**
- `ci-test` depends on: `ci-backend-lint`, `ci-backend-test`, `ci-backend-integration-test`
- Requires: `ci-backend-lint` and `ci-backend-test` must succeed
- Allows: `ci-backend-integration-test` can be skipped (no integration tests found)

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
- `dev`: `ci-backend-lint`, `ci-backend-test`, `ci-test`, `security-scan`
- `staging`: `ci-backend-lint`, `ci-backend-test`, `ci-backend-integration-test`, `ci-test`, `security-scan`
- `main`: `ci-backend-lint`, `ci-backend-test`, `ci-backend-integration-test`, `ci-test`, `security-scan`

### Option 3: Require Individual Jobs Only (Not Recommended)
**Pros:**
- Most granular control

**Cons:**
- No aggregate status check
- More complex to manage
- Doesn't leverage aggregate job logic

## Recommended Configuration

**For `dev` branch:**
- `ci-backend-lint` (required)
- `ci-backend-test` (required)
- `ci-test` (aggregate - verifies all test jobs)
- `security-scan` (aggregate - verifies all security jobs)

**For `staging` branch:**
- `ci-backend-lint` (required)
- `ci-backend-test` (required)
- `ci-backend-integration-test` (required - explicit for staging)
- `ci-test` (aggregate - verifies all test jobs)
- `security-scan` (aggregate - verifies all security jobs)

**For `main` branch:**
- `ci-backend-lint` (required)
- `ci-backend-test` (required)
- `ci-backend-integration-test` (required - explicit for main)
- `ci-test` (aggregate - verifies all test jobs)
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
   - Branch protection uses **job IDs** (e.g., `ci-backend-lint`)
   - Jobs do NOT have `name` fields to ensure status check contexts match job IDs
   - When a job has a `name` field, GitHub creates status checks as `{workflow} / {name} (event)`
   - Without `name`, status checks use just the job ID, matching branch protection requirements
   - **Naming Convention**: `ci-*` prefix for CI Tests, `security-*` prefix for Security Scan

2. **Aggregate Jobs:**
   - Always use `if: always()` to run even if dependencies fail
   - Check dependency results explicitly
   - Report final status based on dependency results

3. **Disabled Jobs:**
   - `frontend-*` jobs are disabled with `if: false`
   - Don't include in branch protection rules
   - Will be enabled when frontend is ready

