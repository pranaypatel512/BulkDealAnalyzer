# RELEASE MANAGEMENT

This file prescribes how releases are prepared, validated, and deployed.

## Branching Model

- `main` → production (always deployable)
- `staging` → pre-prod environment
- Feature branches → PRs → reviewed → merged to staging

## CI Gating

Protect `main` with required status checks:
- lint
- unit tests
- vulnerability scan
- contract tests (if applicable)

## Release Process

1. Merge to `main` triggers `ci/release.yml` (semantic-release)
2. CI builds artifacts, runs migration dry-run on staging, deploys to staging preview and runs smoke-tests
3. Manual approval gate (product + dev lead) to deploy to production
4. Post-deploy synthetic checks run for 30 minutes; if error rate exceeds threshold, rollback

## DB Migration Policy

- All migrations must be idempotent
- Migrations run through a `ci/migration.yml` job:
  - Apply to staging DB
  - Run migration tests
  - Require manual approval for prod

## Feature Flags

- Use flags for risky features with percent rollout

## Rollback

- Document image rollback and DB compensating migration steps in `docs/rollback.md`
- One-click rollback to previous stable image via deployment system

## Changelogs

- Enforce Conventional Commits to automatically generate changelogs and release notes
- Tag releases manually (v0.1.0, v0.2.0, etc.)

## GitHub Projects Integration

- Use GitHub Projects for release planning and tracking
- Create release milestones in GitHub Projects
- Track release progress in Roadmap view
- Link issues to release milestones
- Monitor release readiness in project board

## Simple Release Rule (Solo-Dev Friendly)

**main = always deployable**

- Tag releases manually: `v0.1.0`, `v0.2.0`, etc.
- One-click rollback: previous build
- Write process once in this file
- No complex pipelines needed

## Release Checklist

See `docs/release_checklist.md` for detailed checklist.


