# BulkDeal Analyzer Platform

A comprehensive web platform for analyzing bulk deals data from stock exchanges with advanced filtering, analytics, AI-powered insights, and personalized tracking capabilities.

## What This App Does

BulkDeal Analyzer enables traders, investors, and financial analysts to:
- Automatically fetch and analyze bulk deals data
- Filter deals by type (BUY/SELL), symbol, date range, and quantity
- Track specific stocks through personalized watchlists
- Set up alerts for deals matching criteria
- Get AI-powered insights through natural language queries
- View analytics and visualizations of bulk deals trends

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Next.js 14+ (TypeScript, App Router)
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth
- **Hosting**: Vercel (Frontend), Railway/Render (Backend)
- **AI**: Vercel AI SDK

## How to Run Locally

### Prerequisites

See [PREREQUISITES.md](PREREQUISITES.md) for required tools and setup.

### Quick Start (3 Commands)

```bash
# 1. Check environment
./scripts/check_env.sh

# 2. Bootstrap development environment
./scripts/bootstrap.sh

# 3. Start development servers
# Backend
cd backend && uvicorn app.main:app --reload

# Frontend (in another terminal)
cd frontend && npm run dev
```

## How to Deploy

### Frontend (Vercel)

1. Connect repository to Vercel
2. Configure environment variables
3. Deploy automatically on push to `main`

### Backend (Railway/Render)

1. Connect repository to platform
2. Configure environment variables
3. Set build command: `pip install -r requirements.txt && uvicorn app.main:app`
4. Deploy automatically on push to `main`

## Project Structure

```
bulkdeal-analyzer/
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend
├── docs/             # Documentation
├── scripts/          # Helper scripts
└── tests/            # Tests
```

## Documentation

- [PREREQUISITES.md](dev-doc/PREREQUISITES.md) - Setup requirements
- [docs/decisions.md](docs/decisions.md) - Technical decisions
- [RELEASE.md](RELEASE.md) - Release process
- [SECURITY.md](SECURITY.md) - Security policies

**API docs** (when backend is running): Swagger UI at `/docs`, ReDoc at `/redoc` (e.g. `http://localhost:8000/docs`).

**Migrations**: See [supabase/MIGRATIONS.md](supabase/MIGRATIONS.md) for migration list and how to apply with `supabase db push`.

### Verify backend (smoke test)

With the backend running (e.g. `cd backend && uvicorn app.main:app --reload`):

```bash
./scripts/smoke_test_backend.sh
# Or: BASE_URL=http://localhost:8000 ./scripts/smoke_test_backend.sh
```

Without a server (in-process): `cd backend && pytest tests/test_smoke.py -v`

## Development

### Getting Started

1. **Check Prerequisites**: `./scripts/check_env.sh`
2. **Bootstrap Environment**: `./scripts/bootstrap.sh`
3. **Start Development**: See [DEVELOPMENT_READY.md](dev-doc/DEVELOPMENT_READY.md)

### Development Workflow

- **Main Branch**: Production-ready code (tagged v0.1.0-sprint0)
- **Dev Branch**: Integration branch for features
- **Feature Branches**: Create from `dev` for new features

See [DEVELOPMENT_WORKFLOW.md](.github/DEVELOPMENT_WORKFLOW.md) for detailed workflow.

### Branch Protection

All protected branches (`main`, `dev`, `staging`) require:
- ✅ Pull Request (no direct commits)
- ✅ CI/CD pipeline success
- ✅ Code review approval (1 for dev/staging, 2 for main)

**Setup Branch Protection**:
- Quick Guide: [SETUP_BRANCH_PROTECTION.md](.github/SETUP_BRANCH_PROTECTION.md)
- Detailed Rules: [BRANCH_PROTECTION.md](.github/BRANCH_PROTECTION.md)
- **Create/Update Rules**: `./scripts/create_branch_protection.sh` (recommended)
- **Clear & Recreate**: `./scripts/recreate_branch_protection.sh` (full reset)

### Quick Start

```bash
# Switch to dev branch
git checkout dev

# Create feature branch
git checkout -b feature/your-feature-name

# Start developing!
```

## License

[Add license]


