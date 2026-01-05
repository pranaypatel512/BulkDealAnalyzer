# Branch Protection Rules

This document defines the branch protection rules for BulkDeal Analyzer repository.

## Overview

All protected branches (`main`, `dev`, `staging`) require:
- ✅ Pull Request (no direct commits)
- ✅ CI/CD pipeline success
- ✅ Code review approval (varies by branch)

## Branch Protection Rules

### `main` Branch (Production)

**Purpose**: Production-ready code. Always deployable.

**Protection Rules**:
- ✅ **Require a pull request before merging**
  - Require approvals: **2** (at least 2 reviewers)
  - Dismiss stale pull request approvals when new commits are pushed
  - Require review from Code Owners (if CODEOWNERS file exists)
- ✅ **Require status checks to pass before merging**
  - Required checks:
    - `ci-backend-lint` - Backend code linting (Ruff)
    - `ci-backend-test` - Backend unit tests (Pytest)
    - `ci-backend-integration-test` - Backend integration tests
    - `ci-test` - Combined test status check
    - `security-scan` - Secret and dependency scanning
  - Require branches to be up to date before merging
- ✅ **Require conversation resolution before merging**
- ✅ **Require linear history** (no merge commits, only squash/rebase)
- ✅ **Include administrators** (admins must follow these rules)
- ❌ **Do not allow force pushes**
- ❌ **Do not allow deletions**

**Merge Strategy**:
- Preferred: **Squash and merge** (clean history)
- Alternative: **Rebase and merge** (if needed)
- ❌ **Not allowed**: Merge commit

**Workflow**:
```
feature/* → PR → dev → PR → staging → PR → main
```

---

### `dev` Branch (Development)

**Purpose**: Integration branch for features. All feature branches merge here.

**Protection Rules**:
- ✅ **Require a pull request before merging**
  - Require approvals: **0** (solo development - no approvals needed)
  - Dismiss stale pull request approvals when new commits are pushed
- ✅ **Require status checks to pass before merging**
  - Required checks:
    - `ci-backend-lint` - Backend code linting (Ruff)
    - `ci-backend-test` - Backend unit tests (Pytest)
    - `ci-test` - Combined test status check
    - `security-scan` - Secret and dependency scanning
  - Require branches to be up to date before merging
- ✅ **Require conversation resolution before merging**
- ✅ **Include administrators** (admins must follow these rules)
- ❌ **Do not allow force pushes**
- ❌ **Do not allow deletions**

**Merge Strategy**:
- Preferred: **Squash and merge** (clean history)
- Alternative: **Rebase and merge** (if needed)
- ✅ **Allowed**: Merge commit (for feature branches)

**Workflow**:
```
feature/* → PR (CI checks only) → dev
```

**Note for Solo Development**: The `dev` branch is configured with 0 required approvals to allow solo developers to merge PRs after CI checks pass. When working in a team, you can increase this to 1 approval.

---

### `staging` Branch (Pre-Production)

**Purpose**: Pre-production environment. Testing before production release.

**Protection Rules**:
- ✅ **Require a pull request before merging**
  - Require approvals: **1** (at least 1 reviewer)
  - Dismiss stale pull request approvals when new commits are pushed
- ✅ **Require status checks to pass before merging**
  - Required checks:
    - `ci-backend-lint` - Backend code linting (Ruff)
    - `ci-backend-test` - Backend unit tests (Pytest)
    - `ci-backend-integration-test` - Backend integration tests
    - `ci-test` - Combined test status check
    - `security-scan` - Secret and dependency scanning
  - Require branches to be up to date before merging
- ✅ **Require conversation resolution before merging**
- ✅ **Include administrators** (admins must follow these rules)
- ❌ **Do not allow force pushes**
- ❌ **Do not allow deletions**

**Merge Strategy**:
- Preferred: **Squash and merge** (clean history)
- Alternative: **Rebase and merge** (if needed)
- ✅ **Allowed**: Merge commit (from dev)

**Workflow**:
```
dev → PR (1 approval + CI) → staging → PR (2 approvals + CI) → main
```

---

## Feature Branches

**No Protection**: Feature branches (`feature/*`, `bugfix/*`, `hotfix/*`, `release/*`) are not protected.

**Workflow**:
- Developers can push directly to feature branches
- Must create PR to merge into protected branches
- CI/CD runs on PR creation

---

## Required CI/CD Checks

All protected branches require these status checks to pass:

### Backend Checks
- `ci-backend-lint`: Ruff linting
- `ci-backend-test`: Pytest unit tests
- `ci-backend-integration-test`: Integration tests
- `security-secret-scan`: Gitleaks secret scanning

### Frontend Checks (when implemented)
- `frontend-lint`: ESLint + Prettier
- `frontend-test`: Jest/Vitest unit tests
- `frontend-build`: Next.js build
- `frontend-security-scan`: Dependency vulnerability scan

### General Checks
- `pre-commit`: Pre-commit hook checks
- `secret-scan`: Gitleaks secret scanning

---

## Setup Instructions

### Option 1: GitHub Web UI (Recommended)

1. **Navigate to Repository Settings**:
   - Go to: `https://github.com/pranaypatel512/BulkDealAnalyzer/settings/branches`

2. **Protect `main` Branch**:
   - Click "Add rule"
   - Branch name pattern: `main`
   - Configure as per rules above
   - Click "Create"

3. **Protect `dev` Branch**:
   - Click "Add rule"
   - Branch name pattern: `dev`
   - Configure as per rules above
   - Click "Create"

4. **Protect `staging` Branch**:
   - Click "Add rule"
   - Branch name pattern: `staging`
   - Configure as per rules above
   - Click "Create"

### Option 2: GitHub CLI (gh)

Use the provided script: `scripts/setup_branch_protection.sh`

```bash
# Install GitHub CLI if not installed
# https://cli.github.com/

# Authenticate
gh auth login

# Run setup script
./scripts/setup_branch_protection.sh
```

### Option 3: GitHub API

See `scripts/setup_branch_protection.sh` for API-based setup.

---

## Verification

After setting up branch protection:

1. **Test Direct Push** (should fail):
   ```bash
   git checkout main
   echo "test" >> test.txt
   git add test.txt
   git commit -m "test: direct commit"
   git push origin main  # Should fail
   ```

2. **Test PR Workflow** (should work):
   ```bash
   git checkout -b test/pr-workflow
   echo "test" >> test.txt
   git add test.txt
   git commit -m "test: PR workflow"
   git push origin test/pr-workflow
   # Create PR on GitHub - should require approval and CI checks
   ```

---

## Exceptions

### Hotfix Process

For critical production hotfixes, administrators can temporarily bypass protection:

1. Create hotfix branch from `main`
2. Fix and test
3. Create PR with `[HOTFIX]` prefix
4. Get expedited approval
5. Merge to `main` and `dev`

### Emergency Rollback

In case of critical production issues:
- Administrators can use GitHub's "Bypass branch protection" feature
- Must document reason in PR description
- Post-incident review required

---

## Code Owners

Create `.github/CODEOWNERS` file to automatically request reviews:

```
# Global owners
* @pranaypatel512

# Backend
/backend/ @pranaypatel512

# Frontend
/frontend/ @pranaypatel512

# Documentation
/docs/ @pranaypatel512
*.md @pranaypatel512

# CI/CD
/.github/ @pranaypatel512
```

---

## Summary Table

| Branch | Direct Commits | PR Required | Approvals | CI Required | Force Push | Deletion |
|--------|---------------|-------------|-----------|--------------|------------|----------|
| `main` | ❌ | ✅ | 2 | ✅ | ❌ | ❌ |
| `dev` | ❌ | ✅ | 0 | ✅ | ❌ | ❌ |
| `staging` | ❌ | ✅ | 1 | ✅ | ❌ | ❌ |
| `feature/*` | ✅ | N/A | N/A | On PR | ✅ | ✅ |

---

## References

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub CODEOWNERS Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

