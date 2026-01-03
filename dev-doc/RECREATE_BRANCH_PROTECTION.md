# Recreate Branch Protection Rules

## Quick Reference

### Verified Job IDs

**Security Scan Workflow** (`.github/workflows/security-scan.yml`):
- `secret-scan` - Secret scanning (gitleaks)
- `dependency-scan` - Dependency scanning (npm audit, safety)
- `security-scan` - **Aggregate job** (verifies secret-scan + dependency-scan)

**Tests Workflow** (`.github/workflows/tests.yml`):
- `backend-lint` - Backend linting (ruff)
- `backend-test` - Backend unit tests (pytest)
- `backend-integration-test` - Backend integration tests (pytest)
- `test` - **Aggregate job** (verifies backend-lint + backend-test + backend-integration-test)

## Branch Protection Configuration

### Option 1: Automated Setup (Recommended)

```bash
# 1. Ensure GitHub CLI is installed and authenticated
gh auth login

# 2. Run the setup script
./scripts/setup_branch_protection.sh
```

### Option 2: Manual Setup via GitHub Web UI

1. Navigate to: `https://github.com/pranaypatel512/BulkDealAnalyzer/settings/branches`

2. **For `dev` branch:**
   - Branch name pattern: `dev`
   - ✅ Require a pull request before merging
     - Required approvals: **1**
   - ✅ Require status checks to pass before merging
     - ✅ Require branches to be up to date
     - Select these checks:
       - `backend-lint`
       - `backend-test`
       - `test`
       - `security-scan`

3. **For `staging` branch:**
   - Branch name pattern: `staging`
   - ✅ Require a pull request before merging
     - Required approvals: **1**
   - ✅ Require status checks to pass before merging
     - ✅ Require branches to be up to date
     - Select these checks:
       - `backend-lint`
       - `backend-test`
       - `backend-integration-test`
       - `test`
       - `security-scan`

4. **For `main` branch:**
   - Branch name pattern: `main`
   - ✅ Require a pull request before merging
     - Required approvals: **2**
   - ✅ Require status checks to pass before merging
     - ✅ Require branches to be up to date
     - Select these checks:
       - `backend-lint`
       - `backend-test`
       - `backend-integration-test`
       - `test`
       - `security-scan`

## Verification

After setting up, verify the configuration:

```bash
# Run verification script
./scripts/verify_workflow_jobs.sh

# Check branch protection via GitHub CLI
gh api repos/pranaypatel512/BulkDealAnalyzer/branches/dev/protection
gh api repos/pranaypatel512/BulkDealAnalyzer/branches/staging/protection
gh api repos/pranaypatel512/BulkDealAnalyzer/branches/main/protection
```

## Important Notes

1. **Job IDs vs Display Names:**
   - Use job IDs (e.g., `backend-lint`), NOT display names (e.g., "Backend Lint")
   - Job IDs are the keys in the workflow YAML files

2. **Aggregate Jobs:**
   - `test` and `security-scan` are aggregate jobs that verify their dependencies
   - They use `if: always()` to run even if dependencies fail
   - They check dependency results and report final status

3. **Status Checks Appear After First PR:**
   - Status checks only appear in branch protection settings after workflows run
   - Create a test PR to trigger workflows
   - Wait for workflows to complete (5-10 minutes)
   - Then status checks will be available in branch protection settings

4. **"Waiting" State:**
   - Aggregate jobs wait for dependencies to complete (expected behavior)
   - Status checks will update once dependencies finish
   - See `dev-doc/TROUBLESHOOTING_STATUS_CHECKS.md` for more details

## Troubleshooting

If status checks don't appear:

1. **Check workflows ran:**
   - Go to Actions tab
   - Verify workflows executed

2. **Verify job IDs match:**
   ```bash
   ./scripts/verify_workflow_jobs.sh
   ```

3. **Check branch protection:**
   - Settings → Branches → Edit protection rule
   - Verify required checks match job IDs exactly

4. **Re-run workflows:**
   - Close and reopen PR
   - Or push a new commit

## Related Files

- `scripts/setup_branch_protection.sh` - Automated setup script
- `scripts/verify_workflow_jobs.sh` - Verification script
- `dev-doc/WORKFLOW_JOB_VERIFICATION.md` - Detailed job documentation
- `dev-doc/TROUBLESHOOTING_STATUS_CHECKS.md` - Troubleshooting guide
- `.github/BRANCH_PROTECTION.md` - Detailed protection rules

