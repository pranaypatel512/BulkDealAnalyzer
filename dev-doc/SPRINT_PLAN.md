# Sprint Plan & Feature Development

## Current Status

**Sprint 0**: ✅ COMPLETE
- Foundation setup done
- CI/CD working
- Basic parser and tests
- Branch protection configured

**Sprint 1**: ✅ COMPLETE
- Database Schema & Migrations (#9)
- Backend Core Module (#10)
- Frontend Core Setup (#11)
- Basic Authentication (#12)

**Next**: Sprint 2 - User Management & Core Features

## Sprint 1: Core Infrastructure (Week 1)

### Goal
Complete foundation setup and basic backend/frontend structure

### Tasks

#### 1. Database Schema & Migrations
- [ ] Complete database schema (all tables)
- [ ] Create Supabase migrations
- [ ] Setup RLS policies
- [ ] Test database connection

**Branch**: `feature/database-schema-complete`
**Priority**: High
**Estimate**: 2-3 days

#### 2. Backend Core Module
- [ ] Complete backend core module structure
- [ ] Setup module organization (auth, user, admin, shared)
- [ ] Database connection and models
- [ ] Basic API structure

**Branch**: `feature/backend-core-complete`
**Priority**: High
**Estimate**: 2-3 days

#### 3. Frontend Core Setup
- [ ] Initialize Next.js 14+ with App Router
- [ ] Setup TypeScript configuration
- [ ] Setup Tailwind CSS
- [ ] Create module structure
- [ ] Setup routing

**Branch**: `feature/frontend-core-setup`
**Priority**: High
**Estimate**: 2-3 days

#### 4. Basic Authentication
- [ ] Supabase Auth integration (backend)
- [ ] Supabase Auth integration (frontend)
- [ ] Login/Signup pages
- [ ] Protected routes
- [ ] Auth context

**Branch**: `feature/auth-basic-setup`
**Priority**: High
**Estimate**: 2-3 days

### Deliverables
- Working database with RLS
- Backend API structure
- Frontend app structure
- Basic auth flow

### GitHub Milestone
`Sprint 1 - Core Infrastructure`

---

## Sprint 2: Authentication & User Management (Week 2)

### Goal
Complete authentication and user profile management

### Tasks
- [ ] Login/Signup endpoints
- [ ] Password reset
- [ ] User profile management
- [ ] Frontend auth pages (login, signup, profile)
- [ ] Auth context and protected routes

**GitHub Milestone**: `Sprint 2 - Authentication`

---

## Sprint 3: NSE Data Fetching & Parsing (Week 3)

### Goal
Fetch and parse NSE bulk deals data

### Tasks
- [ ] NSE data fetcher (complete)
- [ ] CSV parser enhancements
- [ ] Data models (complete)
- [ ] Database storage
- [ ] Error handling

**GitHub Milestone**: `Sprint 3 - Data Fetching`

---

## Feature Branch Naming Convention

Based on `dev-doc/BRANCH_STRATEGY.md`:

- **Feature**: `feature/{module}-{description}`
  - Example: `feature/database-schema-complete`
  - Example: `feature/auth-login-implementation`
- **Bugfix**: `bugfix/{module}-{description}`
- **Hotfix**: `hotfix/{description}`

## GitHub Projects Setup

### Recommended Structure

**Project Board**: "BulkDeal Analyzer Development"

**Columns**:
1. 📋 **Backlog** - Planned features and tasks (not started)
2. 📝 **TODO** - Tasks ready to start, assigned to developer
3. 🔄 **In Progress** - Active development
4. 👀 **Review** - PRs open and being reviewed
5. 🧪 **Testing** - Code merged, undergoing testing
6. ✅ **Done** - Complete and verified

**Fields**:
- Sprint (dropdown: Sprint 1, Sprint 2, etc.)
- Priority (dropdown: High, Medium, Low)
- Module (dropdown: Database, Backend, Frontend, Auth, etc.)
- Estimate (number: days)

**Labels**:
- `sprint-1`, `sprint-2`, etc.
- `backend`, `frontend`, `database`, `auth`
- `high-priority`, `blocked`
- `feature`, `bugfix`, `hotfix`

## Development Workflow

1. **Create GitHub Issue** for each task
   - Link to Sprint milestone
   - Add appropriate labels
   - Add to GitHub Project board

2. **Create Feature Branch** from `dev`
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b feature/database-schema-complete
   ```

3. **Develop & Test**
   - Write code
   - Write tests
   - Run CI locally

4. **Create PR** to `dev`
   - Link to GitHub Issue
   - Fill PR template
   - Ensure CI passes

5. **Review & Merge**
   - Code review
   - Address feedback
   - Merge to `dev`

6. **Update GitHub Project**
   - Move card: Backlog → TODO → In Progress → Review → Testing → Done
   - Close issue when moved to "Done"

## Next Steps

1. Setup GitHub Project board
2. Create Sprint 1 milestone
3. Create issues for Sprint 1 tasks
4. Start with highest priority task
5. Create first feature branch

