# Setup Branch Protection - Quick Guide

This guide will help you set up branch protection rules for the BulkDeal Analyzer repository.

## Quick Setup (Recommended)

### Option 1: Automated Setup (GitHub CLI)

```bash
# 1. Install GitHub CLI (if not installed)
# Visit: https://cli.github.com/

# 2. Authenticate
gh auth login

# 3. Run setup script
./scripts/setup_branch_protection.sh
```

### Option 2: Manual Setup (GitHub Web UI)

1. **Navigate to Branch Settings**:
   - Go to: `https://github.com/pranaypatel512/BulkDealAnalyzer/settings/branches`

2. **Add Protection Rule for `main`**:
   - Click "Add rule"
   - Branch name pattern: `main`
   - ✅ **Protect matching branches**
   - ✅ **Require a pull request before merging**
     - ✅ Require approvals: **2**
     - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ **Require status checks to pass before merging**
     - ✅ Require branches to be up to date before merging
     - Select required checks:
       - `backend-lint`
       - `backend-test`
       - `security-scan`
       - `test`
   - ✅ **Require conversation resolution before merging**
   - ✅ **Require linear history**
   - ✅ **Include administrators**
   - ❌ **Do not allow force pushes**
   - ❌ **Do not allow deletions**
   - ✅ **Allow squash merging**
   - ❌ **Do not allow merge commits**
   - ✅ **Allow rebase merging**
   - Click "Create"

3. **Add Protection Rule for `dev`**:
   - Click "Add rule"
   - Branch name pattern: `dev`
   - ✅ **Protect matching branches**
   - ✅ **Require a pull request before merging**
     - ✅ Require approvals: **1**
     - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ **Require status checks to pass before merging**
     - ✅ Require branches to be up to date before merging
     - Select required checks:
       - `backend-lint`
       - `backend-test`
       - `security-scan`
       - `test`
   - ✅ **Require conversation resolution before merging**
   - ✅ **Include administrators**
   - ❌ **Do not allow force pushes**
   - ❌ **Do not allow deletions**
   - Click "Create"

4. **Add Protection Rule for `staging`**:
   - Click "Add rule"
   - Branch name pattern: `staging`
   - ✅ **Protect matching branches**
   - ✅ **Require a pull request before merging**
     - ✅ Require approvals: **1**
     - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ **Require status checks to pass before merging**
     - ✅ Require branches to be up to date before merging
     - Select required checks:
       - `backend-lint`
       - `backend-test`
       - `backend-integration-test`
       - `security-scan`
       - `test`
   - ✅ **Require conversation resolution before merging**
   - ✅ **Include administrators**
   - ❌ **Do not allow force pushes**
   - ❌ **Do not allow deletions**
   - Click "Create"

## Verification

After setting up protection, verify it works:

### Test 1: Direct Push (Should Fail)

```bash
git checkout main
echo "test" >> test.txt
git add test.txt
git commit -m "test: direct commit"
git push origin main
# Expected: ❌ Error - branch is protected
```

### Test 2: PR Workflow (Should Work)

```bash
git checkout -b test/pr-workflow
echo "test" >> test.txt
git add test.txt
git commit -m "test: PR workflow"
git push origin test/pr-workflow
# Create PR on GitHub
# Expected: ✅ PR created, requires approval and CI checks
```

## Required Status Checks

The following status checks must pass before merging:

### For `dev` branch:
- `backend-lint` - Backend code linting
- `backend-test` - Backend unit tests
- `security-scan` - Secret and dependency scanning
- `test` - Combined test status

### For `staging` branch:
- `backend-lint` - Backend code linting
- `backend-test` - Backend unit tests
- `backend-integration-test` - Backend integration tests
- `security-scan` - Secret and dependency scanning
- `test` - Combined test status

### For `main` branch:
- `backend-lint` - Backend code linting
- `backend-test` - Backend unit tests
- `backend-integration-test` - Backend integration tests
- `security-scan` - Secret and dependency scanning
- `test` - Combined test status

**Note**: These checks will appear after the first PR is created and CI workflows run.

## Troubleshooting

### Issue: "No status checks found"

**Solution**: Create a test PR to trigger CI workflows. The status checks will appear after the first workflow run.

### Issue: "Cannot push to protected branch"

**Solution**: This is expected! You must create a Pull Request instead of pushing directly.

### Issue: "Required status checks are not showing"

**Solution**: 
1. Ensure CI workflows are configured (`.github/workflows/`)
2. Create a test PR to trigger workflows
3. Wait for workflows to complete
4. The status checks will appear in branch protection settings

### Issue: "Approval required but no reviewers assigned"

**Solution**: 
1. Add yourself as a code owner in `.github/CODEOWNERS`
2. Or manually request reviewers when creating PR

## Next Steps

1. ✅ Set up branch protection rules
2. ✅ Verify protection is working
3. ✅ Create first feature branch
4. ✅ Test PR workflow

## References

- [Detailed Branch Protection Rules](.github/BRANCH_PROTECTION.md)
- [Branch Strategy](dev-doc/BRANCH_STRATEGY.md)
- [Development Workflow](.github/DEVELOPMENT_WORKFLOW.md)
- [GitHub Branch Protection Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

