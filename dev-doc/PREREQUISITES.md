# PREREQUISITES

This document lists machine, account, and project-level prerequisites that must be verified before development, testing, or release.

## Required Developer Tools (Minimum Supported Versions)

- **git** >= 2.34
- **node** >= 25.2.1 (latest, use .nvmrc to pin)
- **npm** >= 11.7.0 (latest)
- **python** >= 3.14.2
- **docker** >= 20.10
- **docker-compose** >= 1.29 or Docker Compose v2.x
- **supabase CLI** (pin version in TOOL_VERSIONS)
- **jq**, **curl**
- **prek** (pre-commit hook manager - single binary)
- **gitleaks** (secret scanning - install from https://github.com/gitleaks/gitleaks)

## Environment Files

- `.env.example` (must include placeholders for all services)
- Developers must copy `templates/env.example` -> `.env.development` and fill dev credentials
- **NEVER** commit `.env*` files to git

## Accounts and Access

- Ensure dev service accounts created for:
  - Supabase
  - Sentry (optional)
  - Monitoring services
  - MCP servers (if using)
- Add dev accounts to chosen password manager (1Password / Bitwarden) with read-only secrets where appropriate

## Local Dev Start

- `./scripts/bootstrap.sh` must be run once to:
  - Create `.env.development` from template
  - Start local emulators (if docker-compose.yml exists)
  - Seed test data (if available)
- `./scripts/check_env.sh` validates environment on each machine

## Test Data

- Provide `tests/fixtures/` containing:
  - Small canonical CSVs
  - `scripts/generate_large_fixture.py` to simulate heavy uploads
  - Intentionally malformed CSV for error handling tests

## Dev Container

- Provide `.devcontainer/devcontainer.json` for VS Code devcontainers so contributors have identical environments

## Onboarding Checklist for New Devs

1. Clone repo
2. Run `./scripts/check_env.sh` - verify all tools installed
3. Run `./scripts/bootstrap.sh` - setup environment
4. Copy `templates/env.example` to `.env.development` and fill credentials
5. Run `pip install -r requirements.txt` (backend)
6. Run `npm install` or `pnpm install` (frontend)
7. Run `pnpm test` / `pytest` - verify tests pass
8. Start development servers and verify everything works

## Verification

After setup, verify:
- [ ] All tools installed (check_env.sh passes)
- [ ] Environment variables configured (.env.development exists)
- [ ] Dependencies installed (backend and frontend)
- [ ] Tests pass
- [ ] Development servers start successfully


