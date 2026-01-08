# GitHub Projects Setup Guide

## Overview

This guide helps you set up GitHub Projects for tracking features, sprints, and PRs using the branch-based development workflow.

## Quick Setup

### 1. Run the Setup Script

```bash
./scripts/setup_github_project.sh
```

This will:
- ✅ Create Sprint milestones (Sprint 1, Sprint 2, Sprint 3)
- ✅ Create labels (sprint-*, backend, frontend, database, etc.)
- ✅ Create Sprint 1 issues with proper labels and milestones

### 2. Create GitHub Project Board

**Manual Step** (GitHub Projects cannot be fully automated via CLI yet):

1. Go to: `https://github.com/pranaypatel512/BulkDealAnalyzer/projects/new`
2. Choose "Board" template
3. Name: "BulkDeal Analyzer Development"

**Recommended Columns**:
1. 📋 **Backlog** - Planned features and tasks
2. 🔄 **In Progress** - Active development
3. 👀 **In Review** - PRs open and reviewing
4. ✅ **Done** - Merged and completed

### 3. Configure Project Fields

**Add Custom Fields**:
- **Sprint** (Dropdown): Sprint 1, Sprint 2, Sprint 3, etc.
- **Priority** (Dropdown): High, Medium, Low
- **Module** (Dropdown): Database, Backend, Frontend, Auth, User, Admin
- **Estimate** (Number): Days to complete

## Workflow Integration

### Creating a New Feature

1. **Create GitHub Issue**:
   ```bash
   gh issue create \
     --title "Feature Name" \
     --body "Description and acceptance criteria" \
     --milestone "Sprint 1 - Core Infrastructure" \
     --label "sprint-1,backend,high-priority,feature"
   ```

2. **Add Issue to Project Board**:
   - Go to the issue
   - In the right sidebar, add to "BulkDeal Analyzer Development" project
   - Set Sprint, Priority, Module fields

3. **Create Feature Branch**:
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b feature/database-schema-complete
   ```

4. **Link PR to Issue**:
   When creating PR:
   ```bash
   gh pr create \
     --title "feat: Database schema complete" \
     --body "Closes #123" \
     --base dev
   ```

5. **Update Project Card**:
   - Move card from "In Progress" to "In Review"
   - Link PR to card (automatically via PR)

6. **After Merge**:
   - Move card to "Done"
   - Issue auto-closes (if PR says "Closes #123")

## Branch-to-Project Mapping

### Feature Branches
- Branch: `feature/database-schema-complete`
- Issue: #123 "Database Schema & Migrations"
- Project Card: In Sprint 1, Backend module, High priority

### PR Tracking
- PR links to issue: "Closes #123"
- PR automatically appears in "In Review" column
- After merge, card moves to "Done"

## Sprint Planning

### Sprint 1: Core Infrastructure

**Issues** (auto-created by script):
1. Database Schema & Migrations
2. Backend Core Module
3. Frontend Core Setup
4. Basic Authentication

**View Sprint Issues**:
```bash
gh issue list --milestone "Sprint 1 - Core Infrastructure"
```

**View Sprint Progress**:
- Go to GitHub Project board
- Filter by Sprint 1
- See all tasks and their status

## Labels Reference

### Sprint Labels
- `sprint-1` - Sprint 1 tasks
- `sprint-2` - Sprint 2 tasks
- `sprint-3` - Sprint 3 tasks

### Module Labels
- `backend` - Backend module
- `frontend` - Frontend module
- `database` - Database related
- `auth` - Authentication
- `user` - User module
- `admin` - Admin module

### Priority Labels
- `high-priority` - Must complete this sprint
- `medium-priority` - Nice to have
- `low-priority` - Can defer

### Type Labels
- `feature` - New feature
- `bugfix` - Bug fix
- `enhancement` - Enhancement

## Automation (Future)

GitHub Actions can automate:
- Auto-create issues from TODO comments
- Auto-move cards when PR status changes
- Auto-update estimates based on time tracking
- Sprint reports and metrics

## Tips

1. **Always Link PRs to Issues**: Use "Closes #123" in PR description
2. **Keep Cards Updated**: Move cards as work progresses
3. **Use Labels Consistently**: Makes filtering easier
4. **Update Estimates**: Help with sprint planning
5. **Review Sprint Progress**: Weekly sprint reviews using board

## Related Files

- `dev-doc/SPRINT_PLAN.md` - Detailed sprint plan
- `dev-doc/BRANCH_STRATEGY.md` - Branch naming conventions
- `scripts/setup_github_project.sh` - Automated setup script
