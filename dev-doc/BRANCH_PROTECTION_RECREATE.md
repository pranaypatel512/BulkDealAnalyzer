# Recreate Branch Protection Rules - Complete Guide

## Overview

This guide helps you clear and recreate branch protection rules with the correct job IDs that match your GitHub Actions workflows.

## Why Recreate?

After removing `name` fields from workflow jobs, status check contexts changed from:
- ❌ `CI Tests / Backend Lint (pull_request)` (with name field)
- ✅ `backend-lint` (without name field)

Branch protection rules need to be updated to match the new status check context names.

## Quick Recreate (Recommended)

```bash
# One command to clear and recreate everything
./scripts/recreate_branch_protection.sh
```

This script will:
1. ✅ Verify workflows are correctly configured
2. ✅ Clear existing branch protection rules
3. ✅ Wait for GitHub to process
4. ✅ Recreate rules with correct job IDs
5. ✅ Verify the new rules

## Manual Steps

### Step 1: Verify Workflows

```bash
./scripts/verify_workflow_jobs.sh
```

**Expected Output:**
- ✅ All required checks match workflow job IDs
- ✅ No required jobs have 'name' fields
- Status check contexts will be: backend-lint, backend-test, etc.

### Step 2: Clear Existing Rules

```bash
./scripts/clear_branch_protection.sh
```

**Or manually via GitHub CLI:**
```bash
gh api -X DELETE repos/pranaypatel512/BulkDealAnalyzer/branches/main/protection
gh api -X DELETE repos/pranaypatel512/BulkDealAnalyzer/branches/dev/protection
gh api -X DELETE repos/pranaypatel512/BulkDealAnalyzer/branches/staging/protection
```

**Or via GitHub Web UI:**
1. Go to: `https://github.com/pranaypatel512/BulkDealAnalyzer/settings/branches`
2. Delete each protection rule (main, dev, staging)

### Step 3: Recreate Rules

```bash
./scripts/setup_branch_protection.sh
```

**Or manually via GitHub CLI:**
```bash
# See scripts/setup_branch_protection.sh for the exact API calls
```

## Current Job IDs (Status Check Contexts)

### Tests Workflow (`CI Tests`)
- `ci-backend-lint` - Backend linting
- `ci-backend-test` - Backend unit tests
- `ci-backend-integration-test` - Backend integration tests
- `ci-test` - Aggregate job

### Security Scan Workflow (`security-scan`)
- `security-secret-scan` - Secret scanning (gitleaks)
- `security-dependency-scan` - Dependency scanning
- `security-scan` - Aggregate job

## Branch Protection Configuration

### `dev` Branch
**Required Checks:**
- `ci-backend-lint`
- `ci-backend-test`
- `ci-test`
- `security-scan`

**Settings:**
- PR required: ✅
- Approvals: 1
- Force push: ❌
- Deletion: ❌

### `staging` Branch
**Required Checks:**
- `ci-backend-lint`
- `ci-backend-test`
- `ci-backend-integration-test`
- `ci-test`
- `security-scan`

**Settings:**
- PR required: ✅
- Approvals: 1
- Force push: ❌
- Deletion: ❌

### `main` Branch
**Required Checks:**
- `ci-backend-lint`
- `ci-backend-test`
- `ci-backend-integration-test`
- `ci-test`
- `security-scan`

**Settings:**
- PR required: ✅
- Approvals: 2
- Force push: ❌
- Deletion: ❌
- Linear history: ✅

## Verification After Recreate

### 1. Check via GitHub CLI

```bash
# Check main branch
gh api repos/pranaypatel512/BulkDealAnalyzer/branches/main/protection | jq '.required_status_checks.contexts'

# Check dev branch
gh api repos/pranaypatel512/BulkDealAnalyzer/branches/dev/protection | jq '.required_status_checks.contexts'

# Check staging branch
gh api repos/pranaypatel512/BulkDealAnalyzer/branches/staging/protection | jq '.required_status_checks.contexts'
```

### 2. Check via GitHub Web UI

1. Go to: `https://github.com/pranaypatel512/BulkDealAnalyzer/settings/branches`
2. Click on each branch rule
3. Verify required checks match job IDs exactly

### 3. Test with a PR

1. Create a test PR
2. Wait for workflows to run
3. Check that status checks appear with job IDs (not full format)
4. Verify branch protection recognizes them

## Troubleshooting

### Issue: "Status checks still showing full format"

**Solution:**
- Ensure workflows have been updated (no `name` fields)
- Push changes to trigger new workflow runs
- Old workflow runs may still show the old format

### Issue: "Branch protection shows old check names"

**Solution:**
- Clear branch protection rules completely
- Wait a few minutes
- Recreate rules
- Create a new PR to trigger fresh workflows

### Issue: "Some checks still in 'waiting' state"

**Solution:**
1. Verify workflows ran: Check Actions tab
2. Verify job IDs match: Run `./scripts/verify_workflow_jobs.sh`
3. Check branch protection: Ensure job IDs match exactly
4. Wait for workflows to complete (aggregate jobs wait for dependencies)

## Related Scripts

- `scripts/verify_workflow_jobs.sh` - Verify job IDs match
- `scripts/clear_branch_protection.sh` - Clear existing rules
- `scripts/setup_branch_protection.sh` - Create new rules
- `scripts/recreate_branch_protection.sh` - Do everything (clear + recreate)

## Related Documentation

- [Workflow Job Verification](dev-doc/WORKFLOW_JOB_VERIFICATION.md)
- [Troubleshooting Status Checks](dev-doc/TROUBLESHOOTING_STATUS_CHECKS.md)
- [Branch Protection Setup](.github/SETUP_BRANCH_PROTECTION.md)
- [Branch Protection Rules](.github/BRANCH_PROTECTION.md)

