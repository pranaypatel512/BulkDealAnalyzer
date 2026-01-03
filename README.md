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

- [PREREQUISITES.md](PREREQUISITES.md) - Setup requirements
- [docs/decisions.md](docs/decisions.md) - Technical decisions
- [RELEASE.md](RELEASE.md) - Release process
- [SECURITY.md](SECURITY.md) - Security policies

## Development

See [PREREQUISITES.md](PREREQUISITES.md) for development setup.

## License

[Add license]


