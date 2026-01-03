# Branch Strategy

## Branch Types

### Main Branches

- **`main`**: Production-ready code. Always deployable. Protected branch.
- **`dev`**: Development branch. Integration branch for features.

### Supporting Branches

- **`staging`**: Pre-production environment. Testing before production.
- **`feature/*`**: Feature development branches
- **`bugfix/*`**: Bug fix branches
- **`hotfix/*`**: Critical production fixes
- **`release/*`**: Release preparation branches

## Branch Naming Convention

- **Feature**: `feature/{module}-{description}`
  - Example: `feature/auth-login-implementation`
- **Bugfix**: `bugfix/{module}-{description}`
  - Example: `bugfix/user-deals-sorting-issue`
- **Hotfix**: `hotfix/{description}`
  - Example: `hotfix/critical-security-patch`
- **Release**: `release/v{version}`
  - Example: `release/v1.0.0`

## Workflow

1. **Feature Development**:
   - Create branch from `dev`: `git checkout -b feature/auth-login dev`
   - Develop and test
   - Create PR to `dev`
   - After review, merge to `dev`

2. **Release Process**:
   - Create release branch from `dev`: `git checkout -b release/v1.0.0 dev`
   - Final testing and bug fixes
   - Merge to `staging` for staging deployment
   - After validation, merge to `main` and tag

3. **Hotfix Process**:
   - Create branch from `main`: `git checkout -b hotfix/critical-fix main`
   - Fix and test
   - Merge to `main` and `dev`
   - Tag release

## Branch Protection Rules

### `main` Branch
- Require pull request reviews
- Require status checks to pass
- Require branches to be up to date
- No force push
- No deletion

### `dev` Branch
- Require pull request reviews (optional for team)
- Require status checks to pass
- No force push

## Initial Setup

```bash
# Create main branch (already on main after init)
git checkout -b dev
git checkout -b staging
git checkout main

# Push branches
git push -u origin main
git push -u origin dev
git push -u origin staging
```

