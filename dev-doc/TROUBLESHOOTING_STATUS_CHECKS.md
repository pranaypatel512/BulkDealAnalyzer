# Troubleshooting Status Checks "Waiting" State

## Issue
Status checks (`security-scan`, `test`) stuck in "waiting" state in GitHub Actions.

## Root Causes

### 1. Workflows Haven't Run Yet
**Symptom**: Checks show "Expected — Waiting for status to be reported"

**Solution**: 
- Create or update a PR to trigger workflows
- Wait for workflows to complete
- Status checks appear after first workflow run

### 2. Dependency Jobs Still Running
**Symptom**: Aggregate jobs (`security-scan`, `test`) waiting for dependencies

**Solution**: 
- Aggregate jobs use `needs: [job1, job2]` and `if: always()`
- They wait for dependencies to complete before running
- This is expected behavior - wait for dependencies to finish

### 3. Branch Protection Mismatch
**Symptom**: Checks never appear or always show "waiting"

**Solution**:
1. Check branch protection rules match actual job IDs:
   ```bash
   # View actual job IDs in workflows
   grep -E "^  [a-z-]+:" .github/workflows/*.yml
   ```
2. Update branch protection to match:
   - `ci-backend-lint` (not `Backend Lint` or `CI Tests / Backend Lint`)
   - `ci-backend-test` (not `Backend Tests`)
   - `ci-backend-integration-test` (not `Backend Integration Tests`)
   - `ci-test` (not `Test`)
   - `security-scan` (not `Security Scan`)

### 4. Merge Conflicts
**Symptom**: Workflows don't trigger

**Solution**: Resolve merge conflicts in PR

## Current Workflow Configuration

### Security Scan Workflow
- `security-secret-scan`: Runs gitleaks
- `security-dependency-scan`: Runs npm audit, safety check
- `security-scan`: Aggregates results (requires `security-secret-scan` success)

### Tests Workflow
- `ci-backend-lint`: Runs ruff
- `ci-backend-test`: Runs pytest unit tests
- `ci-backend-integration-test`: Runs integration tests
- `ci-test`: Aggregates results (requires `ci-backend-lint` and `ci-backend-test` success)

## Verification Steps

1. **Check Workflow Runs**:
   ```
   GitHub → Actions tab → Check if workflows ran
   ```

2. **Check Job Status**:
   ```
   Click on workflow run → Check individual job statuses
   ```

3. **Check Branch Protection**:
   ```
   GitHub → Settings → Branches → Edit protection rule
   → Verify required checks match job IDs exactly
   ```

4. **Test Locally**:
   ```bash
   ./scripts/test_workflows_local.sh
   ```

## Expected Behavior

1. **First PR**: 
   - Workflows trigger
   - Jobs run
   - Status checks appear after completion
   - May take 5-10 minutes

2. **Subsequent PRs**:
   - Workflows trigger immediately
   - Status checks update as jobs complete
   - Aggregate jobs wait for dependencies (expected)

## If Still Stuck

1. **Check GitHub Actions logs**:
   - Look for errors in workflow runs
   - Check if jobs are actually running

2. **Verify job IDs**:
   ```bash
   # List all job IDs
   grep -E "^  [a-z-]+:" .github/workflows/*.yml | grep -v "on:" | grep -v "runs-on:"
   ```

3. **Update branch protection**:
   - Remove old/incorrect check names
   - Add correct job IDs
   - Save changes

4. **Re-run workflows**:
   - Close and reopen PR
   - Or push a new commit

## Related Files

- `.github/workflows/security-scan.yml`
- `.github/workflows/tests.yml`
- `scripts/setup_branch_protection.sh`
- `.github/BRANCH_PROTECTION.md`

