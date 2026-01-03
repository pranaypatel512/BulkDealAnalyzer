# Development Workflow

## Branch Strategy

### Main Branch
- **Purpose**: Production-ready code
- **Protection**: Required PR reviews, status checks
- **Deployment**: Auto-deploys to production
- **Status**: ✅ Sprint 0 complete, ready for releases

### Dev Branch
- **Purpose**: Integration branch for features
- **Protection**: Status checks required
- **Deployment**: Deploys to staging environment
- **Status**: ✅ Ready for feature development

### Feature Branches
- **Naming**: `feature/{module}-{description}`
- **Example**: `feature/auth-login-implementation`
- **Workflow**: Create from `dev`, develop, PR to `dev`

## Starting Development

### 1. Setup Development Environment
```bash
# Check prerequisites
./scripts/check_env.sh

# Bootstrap environment
./scripts/bootstrap.sh

# Setup environment variables
cp templates/env.example .env.development
# Edit .env.development with your credentials
```

### 2. Create Feature Branch
```bash
# From dev branch
git checkout dev
git pull origin dev

# Create feature branch
git checkout -b feature/{module}-{description}

# Example:
git checkout -b feature/auth-login-implementation
```

### 3. Develop Feature
```bash
# Make changes
# Run tests
cd backend && pytest
cd frontend && npm test

# Check code quality
./scripts/pre_commit_check.sh

# Commit changes
git add .
git commit -m "feat: implement login functionality"
```

### 4. Create Pull Request
```bash
# Push branch
git push -u origin feature/{module}-{description}

# Create PR on GitHub:
# - Base: dev
# - Compare: feature/{module}-{description}
# - Add reviewers
# - Link related issues
```

### 5. After PR Approval
```bash
# Merge to dev (via GitHub UI or CLI)
git checkout dev
git pull origin dev

# Continue with next feature
```

## Release Process

### From Dev to Main
```bash
# 1. Ensure dev is stable
git checkout dev
git pull origin dev

# 2. Create release branch (optional)
git checkout -b release/v1.0.0

# 3. Final testing and fixes

# 4. Merge to main
git checkout main
git merge dev
git tag v1.0.0
git push origin main --tags
```

## Development Commands

### Daily Workflow
```bash
# Start day
git checkout dev
git pull origin dev
git checkout -b feature/new-feature

# During development
./scripts/pre_commit_check.sh  # Before committing
git add .
git commit -m "feat: description"

# End day
git push -u origin feature/new-feature
```

### Testing
```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test

# Integration tests
cd backend && pytest tests/integration

# E2E tests (when configured)
npm run test:e2e
```

## Code Quality

### Before Committing
- [ ] Run pre-commit checks: `./scripts/pre_commit_check.sh`
- [ ] Run tests: `pytest` and `npm test`
- [ ] Check linting: `ruff check .` and `npm run lint`
- [ ] Verify no secrets: gitleaks passes

### Commit Messages
Follow Conventional Commits:
- `feat: add new feature`
- `fix: fix bug`
- `docs: update documentation`
- `refactor: refactor code`
- `test: add tests`

## Current Status

- **Main**: ✅ Sprint 0 complete, tagged v0.1.0-sprint0
- **Dev**: ✅ Ready for feature development
- **Next**: Begin Sprint 1 - Core Infrastructure

