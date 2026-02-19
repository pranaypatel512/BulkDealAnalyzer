# Sprint Plan & Feature Development

## Current Status

**Sprint 0**: ✅ COMPLETE  
- Foundation setup, CI/CD, parser, branch protection

**Sprint 1**: ✅ COMPLETE  
- Database schema & migrations, backend core, frontend core, basic auth

**Sprint 2**: ✅ COMPLETE  
- Auth (login/signup, profile), protected routes, auth context

**Sprint 3**: ✅ COMPLETE  
- NSE bulk deals fetcher, CSV parser, bulk deals API, Analytics (Bulk Deals tab), Fetch from NSE

**Additional (done)**: Watchlist & Alerts (backend + frontend), Analytics tabs (Bulk / Block / Short Selling), single sidebar nav, Profile with Watchlist/Alerts

**Sprint 4**: ✅ COMPLETE  
- Pagination on Analytics, CSV upload (Bulk Deals tab), Export CSV (current page), Block Deals & Short Selling (tables, NSE fetcher, APIs, tabs + Fetch from NSE)

**Sprint 5**: ✅ COMPLETE  
- Backend tests (block_deals, short_selling), full filtered CSV export (all segments), password reset (already in app)

**Sprint 6**: ✅ COMPLETE  
- Export CSV loading state, API docs in README, smoke tests (pytest + script), watchlist migration idempotent, Deal type filter on Analytics

**Next**: Sprint 8 – Admin Module (#39 done via PR #43; #40–#42 open)

---

## Sprint 1: Core Infrastructure (Week 1) — COMPLETE

### Goal
Complete foundation setup and basic backend/frontend structure

### Tasks
- [x] Database schema (all tables), Supabase migrations, RLS
- [x] Backend core module (auth, API structure)
- [x] Frontend core (Next.js App Router, TypeScript, Tailwind, routing)
- [x] Basic auth (Supabase backend + frontend, login/signup, protected routes, auth context)

---

## Sprint 2: Authentication & User Management — COMPLETE

### Tasks
- [x] Login/Signup (Supabase Auth), profile endpoints
- [x] User profile management (backend + frontend)
- [x] Frontend auth pages and auth context
- [x] Protected routes
- [x] Password reset (forgot-password + reset-password pages)

---

## Sprint 3: NSE Data Fetching & Parsing — COMPLETE

### Tasks
- [x] NSE bulk deals fetcher and import
- [x] CSV parser and data models
- [x] Bulk deals API (list, filter, stats, fetch, upload-csv)
- [x] Analytics page with Bulk Deals tab, symbol/date filters, Fetch from NSE

---

## Sprint 4: Analytics Polish & Data Expansion — COMPLETE

### Tasks

- [x] Pagination on Analytics (Previous/Next, page X of Y, total count)
- [x] CSV upload in Analytics (Bulk Deals tab only)
- [x] Export current table to CSV (all three segments)
- [x] Block Deals: tables, NSE BLOCK_DEALS_DATA fetcher, list + fetch API, Analytics tab
- [x] Short Selling: tables, NSE short-deals fetcher, list + fetch API, Analytics tab

---

## Sprint 5: Optional Follow-ups — COMPLETE

### Tasks
- [x] Backend tests for block_deals and short_selling APIs
- [x] Full filtered export (GET …/export-csv with filters, all segments)
- [x] Password reset flow (forgot-password + reset-password pages)
- [x] Tune NSE short-selling response keys + normalize BUY/SELL (implemented later in Sprint 7)

---

## Sprint 6: Polish & Reliability — COMPLETE

### Tasks
- [x] Export CSV loading state and success feedback on Analytics
- [x] API docs documented in README (/docs, /redoc when backend running)
- [x] Smoke tests: backend pytest (test_smoke.py) + scripts/smoke_test_backend.sh
- [x] Watchlist migration idempotent (DROP POLICY IF EXISTS, DROP TRIGGER IF EXISTS)
- [x] Deal type filter on Analytics (All / BUY / SELL)

---

## Sprint 7: Enhancements & Next Features — COMPLETE

### Goal
Add small enhancements and prepare for larger backlog items.

### Tasks
- [x] Document smoke test and migrations in README (scripts/smoke_test_backend.sh, pytest test_smoke.py, supabase/MIGRATIONS.md)
- [x] E2E test (Playwright smoke) – merged in PR #38
- [x] NSE short-selling response keys tune-up: handle key variants + normalize Bought/Sold → BUY/SELL (merged in PR #36)
- [ ] Decide when to run Playwright in CI (optional): manual/local only vs add a GitHub Action job
- [ ] Other PRD items (as prioritized): AI Analyzer, admin panel, subscription tiers

---

## Sprint 8: Admin Module (Current)

### Goal
Admin can manage system and users (basic back-office).

### Tasks
- [x] **#39** Admin roles and RLS – backend `get_current_admin_user`, GET /admin/status, ADMIN_SETUP.md (PR #43)
- [ ] **#40** Backend admin API: user management, data management, system settings
- [ ] **#41** Frontend admin area (route group) with basic dashboard + tables
- [ ] **#42** Admin audit logging (table + record actions + optional UI)

---

## Sprint 9: AI Analyzer (Planned)

### Goal
AI-powered natural language querying and insights over deals data.

### Tasks
- [ ] AI SDK setup + server route for streaming chat
- [ ] Define tool-calls for “query deals / stats / explanations”
- [ ] AI Analyzer UI: chat interface, suggested prompts, loading/streaming UX
- [ ] Safety: rate limits, prompt injection guardrails, logging

---

## Sprint 10: Monetization (Planned)

### Goal
Subscription tiers, feature gating, and billing pages.

### Tasks
- [ ] Subscription plans and gating rules (free/pro/etc.)
- [ ] Stripe integration + webhook handling
- [ ] Billing UI (manage subscription, invoices)
- [ ] Referral system (optional)

---

## Sprint 11: Security & Polish (Planned)

### Goal
Hardening, performance, and quality gates.

### Tasks
- [ ] Expand test coverage (unit + integration) and add a minimal E2E CI gate if desired
- [ ] Observability: structured logging, request IDs, error tracking
- [ ] Performance tuning: pagination defaults, DB indexes, caching strategy (if needed)
- [ ] Documentation: testing guide, runbooks, onboarding

---

## Sprint 12: Marketing Website (Planned / Optional)

### Goal
Public landing pages, docs/resources, and SEO.

### Tasks
- [ ] Landing page + feature pages
- [ ] Blog/resources (optional)
- [ ] Help center/FAQ (optional)

---

## Sprint 13: Launch Preparation (Planned)

### Goal
Prepare for production release workflow.

### Tasks
- [ ] Staging validation checklist + release checklist
- [ ] Load testing + security audit pass
- [ ] Final bug-fix sprint

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

## Next Steps (Sprint 8 or ad-hoc)

1. **Apply migrations** (if not done): `supabase db push`. See [supabase/MIGRATIONS.md](../supabase/MIGRATIONS.md).
2. **Verify backend**: Run `./scripts/smoke_test_backend.sh` with backend up, or `cd backend && pytest tests/test_smoke.py -v`.
3. **Sprint 8**: Continue with #40 (backend admin API), then #41 (frontend admin), then #42 (audit log).
4. **Set first admin**: See [dev-doc/ADMIN_SETUP.md](ADMIN_SETUP.md) to set a user as admin in Supabase.
5. **Optional**: GitHub Project board – move #40–#42 to In Progress as you pick them.

