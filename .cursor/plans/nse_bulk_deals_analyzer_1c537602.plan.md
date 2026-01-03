---
name: ""
overview: ""
todos: []
---

---

name: NSE Bulk Deals Analyzer Platform

overview: "Comprehensive implementation plan for building a multi-tenant web platform with Next.js 14+ App Router, FastAPI backend, Supabase database, authentication, user accounts, admin panel, multi-environment support, localization, AI-powered natural language analyzer, monetization, and security-first architecture. Built with multi-module architecture (backend: core, auth, user, admin, shared modules; frontend: lib/core, modules/auth, modules/user, modules/admin, components, design-system modules) enabling parallel development, independent testing, and scalable maintenance. The project consists of two separate repositories: (1) Application Website - the main product with user dashboard, deals analysis, admin panel, and AI features; (2) Marketing Website - a separate Next.js site for promotion including landing page, blog, case studies, resources, and help center. Includes detailed todos, comprehensive documentation requirements (API, user, developer, operations, security, admin docs), credential management strategy for secure multi-environment credential handling, API versioning and migration strategy for backward compatibility, database migration strategy using Supabase migrations, development rules and practices files for each module, development workflow best practices, Cursor AI development guidelines, git worktree setup for parallel AI agent development, MCP (Model Context Protocol) server integration (browser, GitHub, filesystem, database, testing servers) for enhanced AI agent capabilities, development tools setup (Mailcatcher for email testing, enhanced pre-commit hooks with linting/formatting), Dribbble integration for design system and marketing website inspiration, Nanobanana integration for image generation (marketing graphics, icons, data visualizations, marketing assets), and GitHub Projects integration for sprint management, task tracking, progress monitoring, release planning, and issue management."

todos:

- id: setup-mcp-servers

content: Setup MCP (Model Context Protocol) servers for enhanced AI agent capabilities - configure browser MCP for testing, GitHub MCP for CI/CD, file system MCP for operations, and other relevant MCP servers

status: pending

- id: setup-git-worktree

content: Setup git worktree for parallel AI agent development - create worktrees for each agent stream to enable parallel development without conflicts

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-mcp-servers
- id: setup-secrets-management

content: Setup secret management infrastructure - create .gitignore to exclude .env files, create .env.example templates, setup secrets scanning

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-git-worktree
- id: setup-pre-commit-hooks

content: Setup prek (Rust-based pre-commit alternative) with secret detection (detect-secrets, gitleaks, or truffleHog) and code quality tools (ruff for Python, ESLint/Prettier for TypeScript) to prevent committing secrets and ensure code quality - prek is a single binary with no dependencies, faster than pre-commit

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-secrets-management
- id: setup-mailcatcher

content: Setup Mailcatcher for email testing during development - catches all emails (password resets, welcome emails, alerts) and displays them in web interface instead of sending real emails

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-backend-core
- id: setup-cicd-secrets

content: Configure CI/CD secret management - setup GitHub Secrets, Vercel environment variables, and secret scanning in CI/CD pipeline

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-secrets-management
- id: setup-supabase

content: Setup Supabase project, configure database schema, and initialize authentication

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-git-worktree
                                                                                                                                                                                                                                                                - setup-secrets-management
- id: database-schema

content: Create Supabase database schema with tables for bulk_deals, users, watchlists, alerts, and admin settings

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-supabase
- id: setup-backend-core

content: Initialize FastAPI backend with core module, environment configuration, and Supabase client integration

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-supabase
- id: setup-module-structure

content: Setup multi-module architecture structure - create backend modules (core, auth, user, admin, shared) and frontend modules (lib, modules/auth, modules/user, modules/admin, components, design-system) with proper directory structure and module boundaries

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-backend-core
                                                                                                                                                                                                                                                                - setup-frontend-core
- id: setup-frontend-core

content: Initialize Next.js 14+ with App Router, TypeScript, Tailwind CSS, core module, environment config, and i18n setup

status: pending

- id: setup-design-system-dribbble

content: Setup design system using Dribbble inspiration for marketing website - research landing page designs, create design system reference, integrate Dribbble API if needed, and establish design patterns (Note: This is for marketing website, not application website)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - marketing-website-setup
- id: setup-image-generation-nanobanana

content: Setup Nanobanana for image generation for marketing website - configure for landing page graphics, custom icons, data visualization images, and marketing assets (Note: This is for marketing website, not application website)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - marketing-website-setup
- id: core-module-base

content: Create core module base with shared utilities, database helpers, and common services

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-backend-core
                                                                                                                                                                                                                                                                - setup-module-structure
- id: nse-fetcher

content: Implement NSE data fetching module in core to download bulk deals CSV from NSE website

status: pending

dependencies:

                                                                                                                                                                                                                                                                - core-module-base
- id: parser-models

content: Create data models and CSV parser for bulk deals data with user isolation

status: pending

dependencies:

                                                                                                                                                                                                                                                                - database-schema
                                                                                                                                                                                                                                                                - core-module-base
- id: analyzer-logic

content: Build analysis engine for filtering BUY deals, sorting by quantity, and accumulation tracking

status: pending

dependencies:

                                                                                                                                                                                                                                                                - parser-models
- id: auth-login

content: Implement login endpoint (POST /api/auth/login) with JWT token generation

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-backend-core
                                                                                                                                                                                                                                                                - database-schema
- id: auth-signup

content: Implement signup endpoint (POST /api/auth/signup) with user profile creation

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-backend-core
                                                                                                                                                                                                                                                                - database-schema
- id: auth-password-reset

content: Implement password reset endpoint (POST /api/auth/password-reset)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-backend-core
                                                                                                                                                                                                                                                                - database-schema
- id: auth-profile

content: Implement profile management endpoints (GET/PUT /api/auth/profile)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-backend-core
                                                                                                                                                                                                                                                                - database-schema
- id: auth-settings

content: Implement user settings endpoints (GET/PUT /api/auth/settings)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-backend-core
                                                                                                                                                                                                                                                                - database-schema
- id: auth-middleware

content: Create auth middleware and dependencies for JWT verification and role-based access

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-login
- id: user-deals

content: Implement deals endpoints (GET /api/user/deals) with filtering and sorting

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-middleware
                                                                                                                                                                                                                                                                - parser-models
- id: user-upload

content: Implement file upload endpoint (POST /api/user/upload) for CSV/Excel files

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-middleware
                                                                                                                                                                                                                                                                - parser-models
- id: user-analytics

content: Implement analytics endpoints (GET /api/user/analytics/{symbol})

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-middleware
                                                                                                                                                                                                                                                                - analyzer-logic
- id: user-watchlists

content: Implement watchlist endpoints (GET/POST/DELETE /api/user/watchlists)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-middleware
                                                                                                                                                                                                                                                                - database-schema
- id: user-alerts

content: Implement alerts endpoints (GET/POST/DELETE /api/user/alerts)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-middleware
                                                                                                                                                                                                                                                                - database-schema
- id: user-preferences

content: Implement preferences endpoints (GET/PUT /api/user/preferences)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-middleware
                                                                                                                                                                                                                                                                - database-schema
- id: admin-dashboard

content: Implement admin dashboard endpoint (GET /api/admin/dashboard) with system stats

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-middleware
                                                                                                                                                                                                                                                                - parser-models
- id: admin-users

content: Implement user management endpoints (GET/PUT /api/admin/users)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-middleware
                                                                                                                                                                                                                                                                - database-schema
- id: admin-data

content: Implement data management endpoints (GET/POST/DELETE /api/admin/deals)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-middleware
                                                                                                                                                                                                                                                                - parser-models
                                                                                                                                                                                                                                                                - nse-fetcher
- id: admin-analytics

content: Implement system analytics endpoints (GET /api/admin/analytics)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-middleware
                                                                                                                                                                                                                                                                - analyzer-logic
- id: admin-settings

content: Implement system settings endpoints (GET/PUT /api/admin/settings)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-middleware
                                                                                                                                                                                                                                                                - database-schema
- id: setup-ai-sdk

content: Setup Vercel AI SDK - install AI SDK Core for backend (unified API for text generation, structured objects, tool calls, agents) and AI SDK UI for frontend (chat hooks, generative UI components). Reference AI SDK Cookbook (https://ai-sdk.dev/cookbook) for recipes and templates

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-frontend-core
                                                                                                                                                                                                                                                                - setup-backend-core
- id: ai-service

content: Implement AI service using Vercel AI SDK Core with RAG (Retrieval Augmented Generation) - use generateText, streamText, and tool calling for answering questions about bulk deals data. Follow "Build a RAG Agent" guide and "Natural Language PostgreSQL" template from AI SDK Cookbook

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-ai-sdk
                                                                                                                                                                                                                                                                - user-analytics
                                                                                                                                                                                                                                                                - analyzer-logic
- id: ai-endpoints

content: Implement AI analyzer endpoints using AI SDK Core (POST /api/user/ai/ask with streaming support, GET /api/user/ai/history) - use Next.js API routes with AI SDK streaming. Reference "Stream Text with Chat Prompt" and "Call Tools" recipes from AI SDK Cookbook

status: pending

dependencies:

                                                                                                                                                                                                                                                                - ai-service
                                                                                                                                                                                                                                                                - auth-middleware
                                                                                                                                                                                                                                                                - setup-ai-sdk
- id: fe-auth-login

content: Create login page and LoginForm component with localization

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-frontend-core
                                                                                                                                                                                                                                                                - auth-login
- id: fe-auth-signup

content: Create signup page and SignupForm component with localization

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-frontend-core
                                                                                                                                                                                                                                                                - auth-signup
- id: fe-auth-password-reset

content: Create password reset page and PasswordResetForm component with localization

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-frontend-core
                                                                                                                                                                                                                                                                - auth-password-reset
- id: fe-auth-profile

content: Create profile page and ProfileForm component with localization

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-frontend-core
                                                                                                                                                                                                                                                                - auth-profile
- id: fe-auth-settings

content: Create settings page with localization

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-frontend-core
                                                                                                                                                                                                                                                                - auth-settings
- id: fe-auth-context

content: Create AuthContext and useAuth hook for global auth state management

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-frontend-core
- id: fe-auth-routes

content: Configure auth routes and protected route wrapper

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-auth-login
                                                                                                                                                                                                                                                                - fe-auth-signup
                                                                                                                                                                                                                                                                - fe-auth-context
- id: fe-user-dashboard

content: Create user dashboard page with quick stats and recent deals

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-auth-routes
                                                                                                                                                                                                                                                                - user-deals
- id: fe-user-deals

content: Create deals page with DataTable component, filtering, and sorting

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-auth-routes
                                                                                                                                                                                                                                                                - user-deals
- id: fe-user-analytics

content: Create analytics page with data visualization

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-auth-routes
                                                                                                                                                                                                                                                                - user-analytics
- id: fe-user-watchlists

content: Create watchlists page with add/remove functionality

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-auth-routes
                                                                                                                                                                                                                                                                - user-watchlists
- id: fe-user-alerts

content: Create alerts page with alert configuration

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-auth-routes
                                                                                                                                                                                                                                                                - user-alerts
- id: fe-user-routes

content: Configure user routes

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-user-dashboard
                                                                                                                                                                                                                                                                - fe-user-deals
- id: fe-admin-dashboard

content: Create admin dashboard page with system statistics

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-auth-routes
                                                                                                                                                                                                                                                                - admin-dashboard
- id: fe-admin-users

content: Create user management page with user list and actions

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-auth-routes
                                                                                                                                                                                                                                                                - admin-users
- id: fe-admin-data

content: Create data management page with bulk deals CRUD operations

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-auth-routes
                                                                                                                                                                                                                                                                - admin-data
- id: fe-admin-analytics

content: Create system analytics page with charts and metrics

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-auth-routes
                                                                                                                                                                                                                                                                - admin-analytics
- id: fe-admin-settings

content: Create system settings page

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-auth-routes
                                                                                                                                                                                                                                                                - admin-settings
- id: fe-admin-routes

content: Configure admin routes

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-admin-dashboard
- id: fe-charts-components

content: Build chart components (line, bar, accumulation charts) using Recharts with Nanobanana-generated visualization graphics and icons

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-user-analytics
                                                                                                                                                                                                                                                                - setup-image-generation-nanobanana
- id: fe-charts-integration

content: Integrate charts into analytics and dashboard pages

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-charts-components
- id: fe-ai-chat-component

content: Create AIChat component using Vercel AI SDK UI (useChat hook) - provides message history, input field, streaming support, and tool usage out of the box. Reference "Chatbot Starter Template" and "Share useChat State Across Components" recipes from AI SDK Cookbook

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-user-routes
                                                                                                                                                                                                                                                                - ai-endpoints
                                                                                                                                                                                                                                                                - setup-ai-sdk
- id: fe-ai-analyzer-page

content: Create AI Analyzer page with full chat interface using AI SDK UI components - includes suggested questions, streaming responses, and tool usage visualization. Reference "Render Visual Interface in Chat" and "Markdown Chatbot with Memoization" recipes from AI SDK Cookbook

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-ai-chat-component
- id: fe-ai-localization

content: Add AI analyzer translations to locale files (en, hi)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-ai-analyzer-page
- id: subscription-schema

content: Create database schema for subscriptions, plans, and referral system

status: pending

dependencies:

                                                                                                                                                                                                                                                                - database-schema
- id: subscription-backend

content: Implement subscription management endpoints (plans, subscribe, cancel, upgrade/downgrade)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-middleware
                                                                                                                                                                                                                                                                - subscription-schema
- id: payment-integration

content: Integrate payment gateway (Stripe) for subscription payments

status: pending

dependencies:

                                                                                                                                                                                                                                                                - subscription-backend
- id: referral-system-backend

content: Implement referral system with reward tracking and credit allocation

status: pending

dependencies:

                                                                                                                                                                                                                                                                - subscription-schema
                                                                                                                                                                                                                                                                - auth-middleware
- id: subscription-frontend

content: Create subscription management UI (plans, billing, upgrade/downgrade)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-auth-routes
                                                                                                                                                                                                                                                                - subscription-backend
- id: referral-frontend

content: Create referral UI with referral links, tracking, and rewards display

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-auth-routes
                                                                                                                                                                                                                                                                - referral-system-backend
- id: feature-gating

content: Implement feature gating based on subscription tier (free vs paid)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - subscription-backend
                                                                                                                                                                                                                                                                - user-module
- id: security-rls-policies

content: Implement Row Level Security (RLS) policies for all tables with proper user isolation and admin access

status: pending

dependencies:

                                                                                                                                                                                                                                                                - database-schema
- id: security-rate-limiting

content: Implement API rate limiting middleware with per-user and per-IP limits, different limits for different endpoints

status: pending

dependencies:

                                                                                                                                                                                                                                                                - core-module-base
- id: security-input-validation

content: Implement comprehensive input validation layer with Pydantic models, sanitization, and length checks

status: pending

dependencies:

                                                                                                                                                                                                                                                                - core-module-base
- id: security-headers-middleware

content: Implement security headers middleware (CSP, HSTS, X-Frame-Options, etc.) for all responses

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-backend-core
                                                                                                                                                                                                                                                                - setup-frontend-core
- id: security-audit-logging

content: Implement comprehensive audit logging system for authentication, authorization, and sensitive operations

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-middleware
                                                                                                                                                                                                                                                                - core-module-base
- id: security-encryption

content: Implement encryption for sensitive data at rest and ensure TLS 1.3 for data in transit

status: pending

dependencies:

                                                                                                                                                                                                                                                                - database-schema
                                                                                                                                                                                                                                                                - core-module-base
- id: security-vulnerability-scanning

content: Setup automated dependency vulnerability scanning and code security scanning in CI/CD pipeline

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-backend-core
                                                                                                                                                                                                                                                                - setup-frontend-core
- id: security-password-policy

content: Implement strong password policy enforcement with complexity requirements and password history

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-signup
- id: security-account-lockout

content: Implement account lockout mechanism after failed login attempts with progressive delays

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-login
- id: security-session-management

content: Implement secure session management with timeout, multi-device tracking, and session revocation

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-middleware
- id: security-csrf-protection

content: Implement CSRF protection for state-changing operations with token validation

status: pending

dependencies:

                                                                                                                                                                                                                                                                - auth-middleware
                                                                                                                                                                                                                                                                - setup-frontend-core
- id: security-data-masking

content: Implement data masking for PII in logs, responses, and error messages

status: pending

dependencies:

                                                                                                                                                                                                                                                                - core-module-base
- id: security-secrets-rotation

content: Implement secrets rotation mechanism and secure key management system

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-backend-core
- id: security-penetration-testing

content: Setup penetration testing framework and schedule regular security audits

status: pending

dependencies:

                                                                                                                                                                                                                                                                - security-rls-policies
                                                                                                                                                                                                                                                                - security-rate-limiting
- id: documentation-api

content: Create API documentation - OpenAPI/Swagger specification, endpoint reference, and usage examples

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-backend-core
- id: documentation-user

content: Create user documentation - getting started guide, user guide, FAQ, and tutorials

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-user-routes
- id: documentation-developer

content: Create developer documentation - setup guide, architecture docs, contributing guidelines, and module documentation

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-module-structure
- id: documentation-operations

content: Create operations documentation - deployment guide, monitoring setup, troubleshooting guide, and operational runbooks

status: pending

dependencies:

                                                                                                                                                                                                                                                                - ci-cd-setup
- id: documentation-security

content: Create security documentation - security policy, threat model, and incident response plan

status: pending

dependencies:

                                                                                                                                                                                                                                                                - security-implementation
- id: documentation-admin

content: Create admin documentation - admin user guide and system management guide

status: pending

dependencies:

                                                                                                                                                                                                                                                                - fe-admin-routes
- id: documentation-prerequisites

content: Create PREREQUISITES.md - document required developer tools (git, node, python, docker, supabase CLI), environment files (.env.example), accounts and access requirements, local dev start process, test data setup, dev container configuration, and onboarding checklist for new developers

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-secrets-management
- id: documentation-security-operational

content: Create SECURITY.md - document security controls, operational runbooks (suspected secret leak, vulnerability process), runtime protections (security headers, rate limiting), DB/RLS enforcement, CI security checks (gitleaks, SAST, DAST), vulnerability process with CVSS scoring and SLAs, and security contact information

status: pending

dependencies:

                                                                                                                                                                                                                                                                - security-implementation
- id: documentation-testing-strategy

content: Create TESTING.md - document testing pyramid (unit, integration, contract, E2E, visual regression), testing tools (pytest, Jest, Playwright, schemathesis, Hypothesis), CI integration, test data management, and quality gates (coverage requirements, review requirements)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-pre-commit-hooks
- id: documentation-release-management

content: Create RELEASE.md - document release management process including branching model (main/staging/feature branches), CI gating, release process (semantic-release, migration dry-run, manual approval), DB migration policy (idempotent migrations), feature flags, rollback procedures, and changelog generation (Conventional Commits)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - ci-cd-setup
- id: documentation-tools-support

content: Create TOOLS_AND_SUPPORT.md - document tool versions (.nvmrc, python-version, tool-versions), dev container setup, observability tools (Sentry, Prometheus/Grafana/Datadog, log storage), secrets manager (1Password/Bitwarden), MCP/AI servers documentation, and support process (on-call rotation, alerting thresholds, severity matrix)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-mcp-servers
- id: scripts-check-env

content: Create scripts/check_env.sh - bash script to validate all required developer tools are installed (git, node, npm, python, docker, docker-compose) with version checking and error reporting

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-secrets-management
- id: scripts-bootstrap

content: Create scripts/bootstrap.sh - bash script to bootstrap development environment by copying .env.example to .env.development, starting local containers (supabase emulator, local db), and seeding test data if available

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-supabase
                                                                                                                                                                                                                                                                - scripts-check-env
- id: cicd-security-scan

content: Create .github/workflows/security-scan.yml - GitHub Actions workflow for security scanning including secret scanning (gitleaks), dependency scanning (npm audit, Snyk), and SAST scanning (Bandit for Python, ESLint security rules)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-pre-commit-hooks
- id: cicd-tests

content: Create .github/workflows/tests.yml - GitHub Actions workflow for CI tests including lint and unit tests job, integration tests job with test DB setup, parallel execution where possible, and test result publishing

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-pre-commit-hooks
- id: cicd-release

content: Create .github/workflows/release.yml - GitHub Actions workflow for release management using semantic-release, triggered on push to main, with automatic changelog generation and version tagging

status: pending

dependencies:

                                                                                                                                                                                                                                                                - ci-cd-setup
- id: documentation-release-checklist

content: Create docs/release_checklist.md - release checklist with automated checks (lint, unit tests, integration tests, security scans, contract tests, migration dry-run) and manual checks (product signoff, monitoring dashboards, runbook updates, on-call notification)

status: pending

dependencies:

                                                                                                                                                                                                                                                                - documentation-release-management
- id: documentation-rollback

content: Create docs/rollback.md - rollback plan documenting image rollback procedures, DB compensating migration steps, stakeholder notification process, and post-rollback verification tests

status: pending

dependencies:

                                                                                                                                                                                                                                                                - documentation-release-management
- id: devcontainer-setup

content: Create .devcontainer/devcontainer.json - VS Code devcontainer configuration to normalize development environment with required tools, extensions, and settings for consistent contributor experience

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-secrets-management
- id: test-fixtures-setup

content: Create tests/fixtures/ directory with canonical CSV files for testing, intentionally malformed CSV for graceful failure testing, and scripts/generate_large_fixture.py for load testing with large datasets

status: pending

dependencies:

                                                                - database-schema
- id: setup-github-projects

content: Setup GitHub Projects for project management - create project boards for sprint management, task tracking, progress monitoring, release planning, and issue management. Configure views (Board, Table, Roadmap), fields (Status, Priority, Sprint, Assignee, Labels), workflows, and automation rules

status: pending

dependencies:

                                                                - setup-git-worktree
- id: github-projects-automation

content: Setup GitHub Projects automation - create GitHub Actions workflows for auto-creating issues from branch names, auto-updating project status from PR events, auto-linking PRs to issues, auto-assigning based on patterns, and auto-tracking sprint progress. Configure branch naming conventions, PR templates, and issue templates

status: pending

dependencies:

                                                                - setup-github-projects
                                                                - cicd-tests
- id: decision-documentation

content: Create docs/decisions.md - lock all technical decisions once to avoid rework: backend language (FastAPI/Python), frontend stack (Next.js/TypeScript), database (Supabase), hosting (Vercel/Railway), auth strategy (Supabase Auth), CSV ingestion approach (batch), and what NOT to build in v1. Rule: once written, don't revisit unless blocker

status: pending
- id: marketing-website-setup

content: Setup separate marketing website repository - initialize Next.js 14+ with App Router, TypeScript, Tailwind CSS, and basic structure

status: pending

- id: marketing-design-system

content: Setup marketing website design system using Dribbble inspiration - research marketing site designs, create design system reference, and establish design patterns

status: pending

dependencies:

                                                                                                                                                                                                                                                                - marketing-website-setup
- id: marketing-image-generation

content: Setup Nanobanana for marketing website image generation - configure for landing graphics, blog images, case study visuals, and marketing assets

status: pending

dependencies:

                                                                                                                                                                                                                                                                - marketing-website-setup
- id: marketing-landing-page

content: Create marketing landing page - hero section, features showcase, pricing section, testimonials, and CTA sections using Dribbble design inspiration and Nanobanana-generated graphics

status: pending

dependencies:

                                                                                                                                                                                                                                                                - marketing-design-system
                                                                                                                                                                                                                                                                - marketing-image-generation
- id: marketing-blog

content: Create blog system for marketing website - blog listing page, individual blog post pages, categories, tags, SEO optimization, and content management

status: pending

dependencies:

                                                                                                                                                                                                                                                                - marketing-website-setup
                                                                                                                                                                                                                                                                - marketing-image-generation
- id: marketing-case-studies

content: Create case studies section - case study listing page, individual case study pages with success stories, metrics, and visual content

status: pending

dependencies:

                                                                                                                                                                                                                                                                - marketing-website-setup
                                                                                                                                                                                                                                                                - marketing-image-generation
- id: marketing-resources

content: Create resources section - resource library with downloadable assets, guides, whitepapers, templates, and documentation links

status: pending

dependencies:

                                                                                                                                                                                                                                                                - marketing-website-setup
- id: marketing-help-center

content: Create help center - FAQ section, search functionality, help articles, tutorials, and support contact information

status: pending

dependencies:

                                                                                                                                                                                                                                                                - marketing-website-setup
- id: marketing-seo-optimization

content: Implement SEO optimization for marketing website - meta tags, structured data, sitemap, robots.txt, and performance optimization

status: pending

dependencies:

                                                                                                                                                                                                                                                                - marketing-landing-page
                                                                                                                                                                                                                                                                - marketing-blog
- id: marketing-analytics

content: Setup analytics for marketing website - Google Analytics, conversion tracking, user behavior tracking, and marketing campaign tracking

status: pending

dependencies:

                                                                                                                                                                                                                                                                - marketing-website-setup
- id: marketing-deployment

content: Setup deployment for marketing website - configure Vercel deployment, environment variables, domain configuration, and CDN setup

status: pending

dependencies:

                                                                                                                                                                                                                                                                - marketing-seo-optimization
- id: documentation-project

content: Create project documentation - README.md, CHANGELOG.md, LICENSE, and CONTRIBUTORS.md

status: pending

- id: credential-management-setup

content: Setup credential management system - create credential inventory, setup password manager or encrypted storage, document credential access procedures, and create .env.example templates

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-secrets-management
- id: setup-api-versioning

content: Setup API versioning strategy and migration plan - implement versioning in FastAPI routes, create migration guide for API changes, and document backward compatibility strategy

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-backend-core
- id: setup-database-migrations

content: Setup database migration system - configure Supabase migrations, create migration workflow, setup migration testing, and document migration procedures

status: pending

dependencies:

                                                                                                                                                                                                                                                                - database-schema
- id: create-module-rules-core

content: Create development rules and practices file for core module - coding standards, patterns, testing requirements, and module-specific guidelines

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-module-structure
- id: create-module-rules-auth

content: Create development rules and practices file for auth module - security practices, authentication patterns, testing requirements, and module-specific guidelines

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-module-structure
- id: create-module-rules-user

content: Create development rules and practices file for user module - data access patterns, RLS usage, testing requirements, and module-specific guidelines

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-module-structure
- id: create-module-rules-admin

content: Create development rules and practices file for admin module - admin access patterns, audit logging requirements, testing requirements, and module-specific guidelines

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-module-structure
- id: create-module-rules-frontend

content: Create development rules and practices file for frontend modules - Next.js patterns, Server/Client Component usage, testing requirements, and module-specific guidelines

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-module-structure
- id: create-development-practices

content: Create comprehensive development practices document - coding standards, git workflow, testing practices, code review process, and team collaboration guidelines

status: pending

dependencies:

                                                                                                                                                                                                                                                                - setup-git-worktree

---

## Multi-Module Architecture

### Architecture Overview

The platform follows a **multi-module architecture** with clear separation of concerns, independent modules, and well-defined interfaces. This enables parallel development, easier maintenance, scalability, and team collaboration.

### Architecture Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Loose Coupling**: Modules communicate through well-defined interfaces
3. **High Cohesion**: Related functionality is grouped within modules
4. **Dependency Inversion**: Modules depend on abstractions, not concrete implementations
5. **Interface-Based Design**: Clear contracts between modules
6. **Independent Deployment**: Modules can be developed and tested independently

### Backend Module Structure

```javascript
backend/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── core/                      # Core Module (Foundation)
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration management
│   │   ├── database.py            # Database client and connection
│   │   ├── exceptions.py          # Custom exceptions
│   │   ├── responses.py            # Standardized API responses
│   │   ├── security.py            # Security utilities (encryption, hashing)
│   │   ├── rate_limiter.py        # Rate limiting middleware
│   │   ├── validators.py          # Input validation utilities
│   │   ├── audit_logger.py        # Audit logging service
│   │   ├── encryption.py          # Data encryption/decryption
│   │   ├── masking.py             # PII masking utilities
│   │   ├── nse_fetcher.py         # NSE data fetching
│   │   ├── parser.py              # CSV/Excel parsing
│   │   ├── analyzer.py            # Data analysis engine
│   │   ├── models.py              # Pydantic models
│   │   └── utils.py               # Common utilities
│   │
│   ├── auth/                      # Authentication Module
│   │   ├── __init__.py
│   │   ├── dependencies.py        # Auth dependencies (get_current_user, etc.)
│   │   ├── middleware.py          # Auth middleware
│   │   ├── routes/
│   │   │   ├── login.py           # Login endpoint
│   │   │   ├── signup.py          # Signup endpoint
│   │   │   ├── password_reset.py  # Password reset
│   │   │   ├── profile.py         # Profile management
│   │   │   └── settings.py        # User settings
│   │   ├── mfa.py                 # Multi-factor authentication
│   │   ├── password_policy.py    # Password policy enforcement
│   │   └── models.py              # Auth-specific models
│   │
│   ├── user/                      # User Module
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── deals.py           # Deals endpoints
│   │   │   ├── upload.py          # File upload
│   │   │   ├── analytics.py       # Analytics endpoints
│   │   │   ├── watchlists.py      # Watchlist management
│   │   │   ├── alerts.py          # Alert management
│   │   │   ├── preferences.py     # User preferences
│   │   │   ├── subscriptions.py   # Subscription management
│   │   │   ├── referrals.py       # Referral system
│   │   │   └── ai_analyzer.py     # AI analyzer endpoints
│   │   └── models.py              # User-specific models
│   │
│   ├── admin/                     # Admin Module
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── dashboard.py       # Admin dashboard
│   │   │   ├── users.py           # User management
│   │   │   ├── data.py            # Data management
│   │   │   ├── analytics.py       # System analytics
│   │   │   └── settings.py        # System settings
│   │   └── models.py              # Admin-specific models
│   │
│   └── shared/                    # Shared Module
│       ├── __init__.py
│       ├── constants.py           # Shared constants
│       ├── enums.py               # Shared enums
│       └── types.py               # Shared type definitions
```

### Frontend Module Structure

```javascript
frontend/
├── app/                           # Next.js App Router
│   ├── (auth)/                    # Auth route group
│   │   ├── login/page.tsx
│   │   ├── signup/page.tsx
│   │   ├── password-reset/page.tsx
│   │   ├── profile/page.tsx
│   │   └── settings/page.tsx
│   ├── (user)/                    # User route group
│   │   ├── dashboard/page.tsx
│   │   ├── deals/page.tsx
│   │   ├── analytics/page.tsx
│   │   ├── watchlists/page.tsx
│   │   ├── alerts/page.tsx
│   │   └── ai-analyzer/page.tsx
│   ├── (admin)/                   # Admin route group
│   │   └── admin/
│   │       ├── dashboard/page.tsx
│   │       ├── users/page.tsx
│   │       ├── data/page.tsx
│   │       ├── analytics/page.tsx
│   │       └── settings/page.tsx
│   ├── api/                       # API Routes (if needed)
│   └── layout.tsx                 # Root layout
│
├── src/
│   ├── lib/                       # Core Module (Frontend)
│   │   ├── config/                # Configuration
│   │   ├── services/              # Core services
│   │   │   ├── supabase/         # Supabase clients
│   │   │   ├── api.ts            # API client
│   │   │   └── i18n.ts           # i18n setup
│   │   ├── utils/                # Utilities
│   │   └── types/                 # TypeScript types
│   │
│   ├── modules/                   # Feature Modules
│   │   ├── auth/                  # Auth Module
│   │   │   ├── components/        # Auth components
│   │   │   ├── hooks/            # Auth hooks
│   │   │   └── types.ts          # Auth types
│   │   │
│   │   ├── user/                  # User Module
│   │   │   ├── components/        # User components
│   │   │   ├── hooks/            # User hooks
│   │   │   └── types.ts          # User types
│   │   │
│   │   ├── admin/                 # Admin Module
│   │   │   ├── components/        # Admin components
│   │   │   ├── hooks/            # Admin hooks
│   │   │   └── types.ts          # Admin types
│   │   │
│   │   └── ai/                    # AI Module
│   │       ├── components/        # AI components
│   │       ├── hooks/            # AI hooks
│   │       └── types.ts          # AI types
│   │
│   ├── components/                # Shared Components
│   │   ├── ui/                    # UI components (shadcn/ui style)
│   │   ├── layout/                # Layout components
│   │   └── charts/                # Chart components
│   │
│   ├── design-system/             # Design System Module
│   │   ├── tokens/                # Design tokens
│   │   ├── components/            # Design system components
│   │   └── docs/                  # Design documentation
│   │
│   └── locales/                   # Localization Module
│       ├── en/
│       └── hi/
```

### Module Dependencies

#### Backend Module Dependencies:

```javascript
core (No dependencies)
  ↓
auth (depends on: core)
  ↓
user (depends on: core, auth)
  ↓
admin (depends on: core, auth)
  ↓
shared (used by all modules)
```

#### Frontend Module Dependencies:

```javascript
lib/core (No dependencies)
  ↓
modules/auth (depends on: lib/core)
  ↓
modules/user (depends on: lib/core, modules/auth)
  ↓
modules/admin (depends on: lib/core, modules/auth)
  ↓
modules/ai (depends on: lib/core, modules/user)
  ↓
components/shared (used by all modules)
```

### Module Interfaces

#### Core Module Interface:

```python
# backend/app/core/database.py
class DatabaseInterface:
    async def get_bulk_deals(filters: dict) -> List[BulkDeal]
    async def create_bulk_deal(deal: BulkDealCreate) -> BulkDeal
    # ... other database operations

# backend/app/core/security.py
def hash_password(password: str) -> str
def verify_password(password: str, hashed: str) -> bool
def encrypt_data(data: str) -> str
def decrypt_data(encrypted: str) -> str

# backend/app/core/responses.py
def success_response(data: Any, message: str = None) -> APIResponse
def error_response(message: str, errors: List[dict] = None) -> APIResponse
```

#### Auth Module Interface:

```python
# backend/app/auth/dependencies.py
def get_current_user(token: str) -> User
def require_admin(user: User) -> User
def get_current_user_optional(token: str = None) -> Optional[User]

# backend/app/auth/routes/login.py
@router.post("/api/auth/login")
async def login(credentials: LoginRequest) -> LoginResponse
```

#### User Module Interface:

```python
# backend/app/user/routes/deals.py
@router.get("/api/user/deals")
async def get_deals(
    user: User = Depends(get_current_user),
    filters: DealFilters = Depends()
) -> DealsResponse
```

### Module Communication

#### 1. **Direct Import** (Within same layer):

```python
# User module imports from Auth module
from app.auth.dependencies import get_current_user
```

#### 2. **Interface-Based** (Cross-module):

```python
# Modules use core interfaces
from app.core.database import DatabaseInterface
from app.core.responses import success_response
```

#### 3. **Dependency Injection** (FastAPI):

```python
# FastAPI dependency injection
@router.get("/api/user/deals")
async def get_deals(user: User = Depends(get_current_user)):
    # user is injected by FastAPI
    pass
```

### Module Responsibilities

#### Core Module:

- Database connection and queries
- Security utilities (encryption, hashing, masking)
- Rate limiting
- Input validation
- Audit logging
- NSE data fetching
- Data parsing and analysis
- Standardized API responses
- Common utilities

#### Auth Module:

- User authentication (login, signup, password reset)
- JWT token management
- Session management
- MFA implementation
- Password policy enforcement
- Account lockout
- Profile management
- User settings

#### User Module:

- Bulk deals viewing and filtering
- File upload handling
- Analytics and data visualization
- Watchlist management
- Alert configuration
- User preferences
- Subscription management
- Referral system
- AI analyzer integration

#### Admin Module:

- System dashboard
- User management (CRUD operations)
- Data management (bulk deals CRUD)
- System analytics
- System settings
- Subscription plan management

#### Shared Module:

- Common constants
- Shared enums
- Shared type definitions
- Cross-module utilities

### Module Development Guidelines

1. **Module Independence**:

- Each module should be independently testable
- Modules should not directly import from other feature modules
- Use interfaces and dependency injection

2. **Interface Contracts**:

- Define clear interfaces for module communication
- Document all public APIs
- Version interfaces for backward compatibility

3. **Error Handling**:

- Modules should handle their own errors
- Use core module's exception handling
- Return standardized error responses

4. **Testing**:

- Each module should have its own test suite
- Mock dependencies when testing
- Integration tests for module interactions

5. **Documentation**:

- Document module purpose and responsibilities
- Document public interfaces
- Document dependencies and usage examples

### Module Deployment Strategy

1. **Monolithic Deployment** (Initial):

- All modules deployed together
- Single FastAPI application
- Single Next.js application

2. **Microservices** (Future - Optional):

- Each module can be split into separate services
- API Gateway for routing
- Service-to-service communication

### Module Versioning

- **Semantic Versioning**: Major.Minor.Patch
- **Breaking Changes**: Increment major version
- **New Features**: Increment minor version
- **Bug Fixes**: Increment patch version

### Module Ownership

Each module can be assigned to different developers/agents:

- **Core Module**: Infrastructure team
- **Auth Module**: Security team
- **User Module**: User features team
- **Admin Module**: Admin features team
- **Frontend Modules**: Frontend team per module

---

## Application vs Marketing Website Separation

### Overview

The project consists of two completely separate repositories to maintain clear separation of concerns, independent deployment cycles, and different management strategies:

1. **Application Website Repository** (`nse-bulk-deals-analyzer`): The main product application
2. **Marketing Website Repository** (`nse-bulk-deals-analyzer-marketing`): The promotional and marketing website

### Why Separate Repositories?

1. **Independent Development**: Marketing website can be updated frequently for campaigns without affecting the application
2. **Different Deployment Cycles**: Marketing site can deploy multiple times per day, while application follows stricter release cycles
3. **Different Teams**: Marketing team can work independently without access to application codebase
4. **Different Tech Requirements**: Marketing site may have different dependencies, build processes, and optimizations
5. **Security**: Marketing site doesn't need access to application secrets, database connections, or internal APIs
6. **Performance**: Marketing site can be optimized for SEO and content delivery without application overhead
7. **Scalability**: Each repository can scale independently based on traffic patterns

### Repository Structure

#### Application Website Repository (`nse-bulk-deals-analyzer`)

```javascript
nse-bulk-deals-analyzer/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── core/
│   │   ├── auth/
│   │   ├── user/
│   │   ├── admin/
│   │   └── shared/
│   └── ...
├── frontend/                   # Next.js application frontend
│   ├── app/
│   │   ├── (auth)/            # Auth routes (login, signup, etc.)
│   │   ├── (user)/            # User routes (dashboard, deals, etc.)
│   │   └── (admin)/           # Admin routes
│   └── ...
├── .github/                    # CI/CD workflows
├── docs/                       # Application documentation
└── ...
```

**Purpose**: Main product application with user authentication, dashboard, deals analysis, admin panel, AI features, and all business logic.**Deployment**:

- Frontend: Vercel (app.nseanalyzer.com)
- Backend: Railway/Render/Cloud Run (api.nseanalyzer.com)

#### Marketing Website Repository (`nse-bulk-deals-analyzer-marketing`)

```javascript
nse-bulk-deals-analyzer-marketing/
├── app/                        # Next.js App Router
│   ├── (marketing)/           # Marketing route group
│   │   ├── page.tsx          # Landing page
│   │   ├── blog/             # Blog section
│   │   │   ├── page.tsx      # Blog listing
│   │   │   └── [slug]/       # Individual posts
│   │   ├── case-studies/     # Case studies section
│   │   │   ├── page.tsx      # Case studies listing
│   │   │   └── [slug]/       # Individual case studies
│   │   ├── resources/        # Resources section
│   │   │   ├── page.tsx      # Resources listing
│   │   │   └── [category]/   # Resource categories
│   │   └── help/             # Help center
│   │       ├── page.tsx      # Help center home
│   │       ├── faq/          # FAQ section
│   │       └── [article]/     # Help articles
│   └── ...
├── content/                    # Content management
│   ├── blog/                 # Blog posts (MDX/Markdown)
│   ├── case-studies/         # Case study content
│   ├── resources/            # Resource files
│   └── help/                 # Help articles
├── components/                # Marketing-specific components
│   ├── marketing/            # Marketing components
│   ├── blog/                 # Blog components
│   └── ...
├── lib/                       # Utilities and services
│   ├── content/              # Content management utilities
│   ├── seo/                  # SEO utilities
│   └── analytics/            # Analytics utilities
├── public/                    # Static assets
│   ├── images/               # Marketing images
│   └── resources/            # Downloadable resources
├── .github/                   # CI/CD workflows
└── ...
```

**Purpose**: Marketing and promotional website with landing page, blog, case studies, resources, and help center.**Deployment**:

- Vercel (www.nseanalyzer.com or nseanalyzer.com)

### Shared Resources

While repositories are separate, they can share:

1. **Design System**: Marketing site can reference design tokens and patterns (via npm package or shared design system repo)
2. **Brand Assets**: Logos, colors, typography guidelines (via shared assets repository or CDN)
3. **Content API**: Marketing site can fetch dynamic content from application API (public endpoints only)
4. **Analytics**: Both can share analytics account for unified tracking

### Management Strategy

#### Application Website Management

- **Development**: Feature-driven development with strict testing and code review
- **Deployment**: Staged deployments (dev → staging → production) with approval gates
- **Monitoring**: Application performance monitoring, error tracking, user analytics
- **Security**: Strict security practices, secret management, vulnerability scanning
- **Versioning**: Semantic versioning for releases
- **Documentation**: Technical documentation, API docs, developer guides

#### Marketing Website Management

- **Development**: Content-driven development with quick iterations
- **Deployment**: Direct deployment to production for content updates, staged for major changes
- **Monitoring**: SEO monitoring, page performance, conversion tracking, traffic analytics
- **Security**: Basic security practices, SEO security, content security
- **Versioning**: Content versioning, A/B testing for landing pages
- **Documentation**: Content guidelines, SEO best practices, marketing workflows

### Integration Points

1. **Authentication Redirect**: Marketing site "Sign Up" button redirects to application website
2. **API Integration**: Marketing site can fetch public data (pricing, features) from application API
3. **Analytics**: Shared analytics account for cross-site tracking
4. **Domain Strategy**: 

- Marketing: `www.nseanalyzer.com` or `nseanalyzer.com`
- Application: `app.nseanalyzer.com`
- API: `api.nseanalyzer.com`

### Development Workflow

#### Application Website

1. Feature development in feature branches
2. Code review and testing
3. Deploy to staging environment
4. QA and approval
5. Deploy to production
6. Monitor and iterate

#### Marketing Website

1. Content creation/updates
2. Preview and review
3. Deploy to production
4. Monitor SEO and conversions
5. A/B test and optimize

### Content Management

#### Application Website

- User-generated content (deals data, watchlists, alerts)
- Admin-managed content (system settings, announcements)
- Database-driven content

#### Marketing Website

- Markdown/MDX files for blog posts
- JSON/Markdown for case studies
- Static files for resources
- Headless CMS option (Contentful, Sanity) for non-technical team members

### SEO Strategy

#### Application Website

- Focus on authenticated user experience
- Minimal SEO requirements (login/signup pages)
- Internal search and navigation

#### Marketing Website

- Full SEO optimization
- Content marketing (blog, case studies)
- Landing pages for different campaigns
- Resource library for backlinks
- Help center for long-tail keywords

### Analytics Strategy

#### Application Website

- User behavior tracking
- Feature usage analytics
- Performance monitoring
- Error tracking
- Business metrics (subscriptions, referrals)

#### Marketing Website

- Traffic analytics
- Conversion tracking
- SEO performance
- Content engagement metrics
- Campaign performance
- User journey tracking

### Deployment Strategy

#### Application Website

- **Frontend**: Vercel with preview deployments for PRs
- **Backend**: Railway/Render/Cloud Run with blue-green deployment
- **Database**: Supabase (managed)
- **CDN**: Vercel Edge Network
- **Monitoring**: Sentry, Datadog, or similar

#### Marketing Website

- **Frontend**: Vercel with instant deployments
- **CDN**: Vercel Edge Network + Cloudflare for global distribution
- **CMS**: Optional headless CMS integration
- **Monitoring**: Google Analytics, Vercel Analytics, SEO tools

### Environment Variables

#### Application Website

- Database credentials
- API keys (Supabase, OpenAI, Stripe)
- JWT secrets
- Service credentials
- Environment-specific configs

#### Marketing Website

- Analytics keys (Google Analytics, etc.)
- Optional CMS credentials
- API keys for public endpoints only
- SEO configuration
- Social media API keys (if needed)

### Best Practices

1. **Clear Boundaries**: Keep repositories completely separate - no shared code dependencies
2. **Independent CI/CD**: Each repository has its own CI/CD pipeline
3. **Separate Teams**: Marketing team doesn't need access to application repository
4. **Content Strategy**: Marketing site focuses on content, application focuses on functionality
5. **Performance**: Optimize each site for its specific purpose
6. **Security**: Application has strict security, marketing has basic security
7. **Documentation**: Maintain separate documentation for each repository

---

## Prerequisites Before Development

### Overview

Before starting actual feature development, it's critical to establish a solid foundation. This section outlines all prerequisites, setup steps, and foundational work that must be completed to ensure smooth development and avoid technical debt, security issues, and development bottlenecks.

### Critical Prerequisites Checklist

#### 1. Development Environment Setup

**Required Tools**:

- **Git**: Version control system
- **Node.js**: v20+ (LTS) for frontend development
- **Python**: v3.11+ for backend development
- **Docker** (Optional): For local services (Mailcatcher, Adminer)
- **prek**: Pre-commit hook manager (single binary, no dependencies)
- **Supabase CLI**: For database migrations and local development
- **Code Editor**: VS Code or Cursor with recommended extensions

**Verification**:

```bash
# Check all tools are installed
node --version    # Should be v20+
python --version  # Should be v3.11+
git --version
prek --version
supabase --version
```

#### 2. Repository Structure & Initialization

**Application Repository** (`nse-bulk-deals-analyzer`):

- Initialize git repository
- Setup `.gitignore` for Python, Node.js, and environment files
- Create initial directory structure (backend/, frontend/)
- Setup branch protection rules (main, develop)
- Initialize README.md with project overview

**Marketing Repository** (`nse-bulk-deals-analyzer-marketing`):

- Initialize separate git repository
- Setup `.gitignore` for Next.js
- Create initial directory structure
- Setup branch protection rules

**Both Repositories**:

- Setup `.editorconfig` for consistent formatting
- Create `CONTRIBUTING.md` with development guidelines
- Setup issue templates (bug, feature, question)

#### 3. Secret Management Infrastructure

**Must Complete Before Any Development**:

- [ ] Create `.env.example` files for all environments
- [ ] Setup `.gitignore` to exclude `.env*` files
- [ ] Configure prek with secret detection hooks (detect-secrets, gitleaks)
- [ ] Document all required environment variables
- [ ] Setup secure credential storage (1Password, Bitwarden, or similar)
- [ ] Create credential inventory document
- [ ] Setup CI/CD secret management (GitHub Secrets, Vercel env vars)

**Why Critical**: Prevents accidental secret commits, security breaches, and deployment failures.

#### 4. Pre-commit Hooks Setup (prek)

**Must Complete Before First Commit**:

- [ ] Install prek binary
- [ ] Create `.pre-commit-config.yaml` with:
- Secret detection (detect-secrets/gitleaks)
- Python linting (ruff)
- Python formatting (ruff format)
- TypeScript linting (ESLint)
- TypeScript formatting (Prettier)
- Type checking (mypy, tsc)
- [ ] Run `prek install` to setup git hooks
- [ ] Test hooks with `prek run --all-files`
- [ ] Document hook configuration

**Why Critical**: Ensures code quality from day one, prevents bad code patterns, catches errors early.

#### 5. Project Structure & Module Architecture

**Must Define Before Development**:

- [ ] Create backend module structure (core, auth, user, admin, shared)
- [ ] Create frontend module structure (lib/core, modules/auth, modules/user, modules/admin)
- [ ] Define module boundaries and dependencies
- [ ] Create module interface contracts
- [ ] Document module communication patterns
- [ ] Setup module-specific `RULES.md` files

**Why Critical**: Prevents architectural drift, enables parallel development, ensures maintainability.

#### 6. Database Schema Design

**Must Complete Before Backend Development**:

- [ ] Design complete database schema (all tables, relationships)
- [ ] Define Row Level Security (RLS) policies
- [ ] Create migration strategy
- [ ] Setup Supabase project
- [ ] Create initial migrations
- [ ] Document schema decisions
- [ ] Create database diagram

**Why Critical**: Schema changes are expensive later, RLS policies are complex, migrations must be planned.

#### 7. API Design & Contracts

**Must Define Before Backend/Frontend Development**:

- [ ] Design all API endpoints (routes, methods, parameters)
- [ ] Define request/response schemas (Pydantic models)
- [ ] Document API versioning strategy
- [ ] Create OpenAPI/Swagger specification
- [ ] Define error response format
- [ ] Setup API client structure (frontend)
- [ ] Create API mock data for frontend development

**Why Critical**: Enables parallel backend/frontend development, prevents integration issues, ensures consistency.

#### 8. Authentication & Authorization Strategy

**Must Define Before Auth Development**:

- [ ] Choose authentication method (Supabase Auth)
- [ ] Design JWT token structure
- [ ] Define role-based access control (RBAC) roles
- [ ] Plan session management
- [ ] Design password policy
- [ ] Plan MFA strategy (for admins)
- [ ] Document auth flow diagrams

**Why Critical**: Auth is foundational, changes are disruptive, security-critical.

#### 9. Environment Configuration

**Must Setup Before Development**:

- [ ] Create environment configuration system (Pydantic Settings)
- [ ] Define all environment variables
- [ ] Setup `.env.development`, `.env.staging`, `.env.production`
- [ ] Create environment validation
- [ ] Document environment setup process
- [ ] Setup environment-specific configurations

**Why Critical**: Prevents configuration errors, enables multi-environment support, ensures consistency.

#### 10. Testing Infrastructure

**Must Setup Before Feature Development**:

- [ ] Choose testing frameworks (pytest, Jest, Playwright)
- [ ] Setup test directory structure
- [ ] Configure test runners
- [ ] Create test utilities and fixtures
- [ ] Setup test database (separate from dev)
- [ ] Configure code coverage tools
- [ ] Document testing guidelines

**Why Critical**: Testing is harder to add later, ensures quality from start, enables TDD.

#### 11. CI/CD Pipeline Foundation

**Must Setup Early**:

- [ ] Create GitHub Actions workflows
- [ ] Setup automated testing on PR
- [ ] Configure linting/formatting checks
- [ ] Setup deployment pipelines (staging, production)
- [ ] Configure secret management in CI/CD
- [ ] Setup deployment notifications
- [ ] Document CI/CD process

**Why Critical**: Prevents broken code in main branch, enables automated deployments, catches issues early.

#### 12. Error Handling & Logging Strategy

**Must Define Before Development**:

- [ ] Design error response format
- [ ] Choose logging library (structlog, winston)
- [ ] Define log levels and structure
- [ ] Plan error tracking (Sentry, Rollbar)
- [ ] Design exception hierarchy
- [ ] Create error handling utilities
- [ ] Document error handling patterns

**Why Critical**: Consistent error handling prevents confusion, logging is essential for debugging.

#### 13. Code Quality Standards

**Must Establish Before Development**:

- [ ] Define coding standards (PEP 8, TypeScript strict mode)
- [ ] Setup linters (ruff, ESLint)
- [ ] Setup formatters (ruff format, Prettier)
- [ ] Configure type checkers (mypy, tsc)
- [ ] Create code review checklist
- [ ] Document code style guide
- [ ] Setup editor configurations (.editorconfig, .vscode/settings.json)

**Why Critical**: Prevents code quality issues, ensures consistency, makes reviews easier.

#### 14. Documentation Structure

**Must Create Before Development**:

- [ ] Create documentation directory structure
- [ ] Setup documentation tools (MkDocs, Docusaurus, or similar)
- [ ] Create API documentation template
- [ ] Create developer setup guide
- [ ] Create architecture documentation template
- [ ] Plan documentation workflow
- [ ] Setup documentation deployment

**Why Critical**: Documentation is harder to write later, ensures knowledge sharing, onboarding.

#### 15. Monitoring & Observability Setup

**Must Plan Before Launch**:

- [ ] Choose monitoring tools (Sentry, Datadog, or similar)
- [ ] Design metrics to track
- [ ] Plan alerting strategy
- [ ] Setup application performance monitoring (APM)
- [ ] Plan log aggregation
- [ ] Design dashboards
- [ ] Document monitoring strategy

**Why Critical**: Essential for production, helps identify issues early, enables data-driven decisions.

#### 16. Security Foundation

**Must Implement Early**:

- [ ] Review OWASP Top 10
- [ ] Plan security headers (CSP, HSTS, etc.)
- [ ] Design rate limiting strategy
- [ ] Plan input validation approach
- [ ] Design audit logging
- [ ] Plan security testing strategy
- [ ] Document security practices

**Why Critical**: Security is harder to retrofit, prevents vulnerabilities, protects users.

#### 17. Performance Optimization Strategy

**Must Plan Early**:

- [ ] Define performance targets (page load, API response times)
- [ ] Plan caching strategy
- [ ] Design database indexing strategy
- [ ] Plan CDN usage
- [ ] Design asset optimization
- [ ] Plan lazy loading strategy
- [ ] Document performance guidelines

**Why Critical**: Performance issues are expensive to fix later, affects user experience.

#### 18. Localization Setup

**Must Setup Before UI Development**:

- [ ] Choose i18n library (next-intl)
- [ ] Setup locale structure
- [ ] Create translation files template
- [ ] Plan translation workflow
- [ ] Setup locale detection
- [ ] Document localization process

**Why Critical**: Adding i18n later requires refactoring, ensures internationalization from start.

### Prerequisites Execution Order

**Phase 1: Foundation (Week 1)**:

1. Development environment setup
2. Repository structure & initialization
3. Secret management infrastructure
4. Pre-commit hooks setup (prek)
5. Project structure & module architecture

**Phase 2: Design & Planning (Week 1-2)**:

6. Database schema design
7. API design & contracts
8. Authentication & authorization strategy
9. Environment configuration
10. Error handling & logging strategy

**Phase 3: Infrastructure (Week 2)**:

11. Testing infrastructure
12. CI/CD pipeline foundation
13. Code quality standards
14. Documentation structure

**Phase 4: Advanced Setup (Week 2-3)**:

15. Monitoring & observability setup
16. Security foundation
17. Performance optimization strategy
18. Localization setup

### Prerequisites Validation

Before starting feature development, validate:

- [ ] All tools installed and working
- [ ] Both repositories initialized
- [ ] Secret management configured
- [ ] Pre-commit hooks working (`prek run --all-files` passes)
- [ ] Module structure created
- [ ] Database schema designed and documented
- [ ] API contracts defined
- [ ] Auth strategy documented
- [ ] Environments configured
- [ ] Testing infrastructure ready
- [ ] CI/CD pipeline working
- [ ] Documentation structure created

### Common Pitfalls to Avoid

1. **Starting Development Too Early**: Starting features before prerequisites leads to:

- Technical debt
- Security vulnerabilities
- Integration issues
- Refactoring costs

2. **Skipping Secret Management**: Leads to:

- Accidental secret commits
- Security breaches
- Deployment failures

3. **Ignoring Pre-commit Hooks**: Leads to:

- Code quality issues
- Inconsistent formatting
- Type errors in production

4. **Undefined API Contracts**: Leads to:

- Backend/frontend mismatches
- Integration delays
- Breaking changes

5. **Poor Database Design**: Leads to:

- Performance issues
- Migration complexity
- Data integrity problems

### Prerequisites Checklist Template

Create a `PREREQUISITES.md` file in each repository with:

```markdown
# Prerequisites Checklist

## Development Environment
- [ ] Node.js v20+ installed
- [ ] Python v3.11+ installed
- [ ] Git configured
- [ ] prek installed
- [ ] Supabase CLI installed

## Repository Setup
- [ ] Repository initialized
- [ ] .gitignore configured
- [ ] Branch protection rules setup
- [ ] README.md created

## Secret Management
- [ ] .env.example created
- [ ] .gitignore excludes .env files
- [ ] Pre-commit hooks configured
- [ ] Credential storage setup

## ... (continue for all prerequisites)
```

---

## Frontend Technology Stack

### Overview

The frontend technology stack is carefully selected to provide rich functionality, easy integration, excellent charting capabilities, and modern development experience. This section details all frontend libraries, tools, and frameworks used in both the Application Website and Marketing Website.

### Core Framework & Build Tools

#### Application Website

- **Next.js 14+**: React framework with App Router
- Server Components for performance
- Server Actions for mutations
- Built-in API routes
- Image optimization
- Font optimization
- Route handlers
- **TypeScript**: Type-safe JavaScript
- Strict mode enabled
- Type checking in CI/CD
- Type generation from API schemas
- **Tailwind CSS**: Utility-first CSS framework
- Custom design system
- Responsive design utilities
- Dark mode support
- **React 18+**: UI library
- Concurrent features
- Suspense for data fetching
- Server Components support

#### Marketing Website

- **Next.js 14+**: Same as application website
- **TypeScript**: Same as application website
- **Tailwind CSS**: Same as application website
- **MDX**: For blog posts and content
- **Content Collections**: For managing blog/case studies content

### Chart & Data Visualization Libraries

#### Primary Chart Library: Recharts

**Why Recharts**:

- Built on D3.js and React
- Declarative API
- Responsive by default
- TypeScript support
- Active maintenance
- Rich chart types
- Customizable

**Installation**:

```bash
npm install recharts
```

**Chart Types Available**:

- **Line Charts**: For trends over time (deal quantities, prices)
- **Bar Charts**: For comparisons (top symbols, deal types)
- **Area Charts**: For accumulation tracking
- **Pie/Donut Charts**: For distribution (deal types, symbol distribution)
- **Scatter Charts**: For correlations
- **Composed Charts**: Multiple chart types combined
- **Radial Charts**: For circular data visualization

**Usage Example**:

```typescript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export function DealTrendChart({ data }: { data: DealData[] }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="quantity" stroke="#8884d8" />
        <Line type="monotone" dataKey="price" stroke="#82ca9d" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

#### Alternative/Complementary Libraries

**Chart.js** (Optional, for specific use cases):

- Simpler API for basic charts
- Good for quick prototypes
- Installation: `npm install chart.js react-chartjs-2`

**D3.js** (For advanced custom visualizations):

- Maximum flexibility
- For complex, custom charts
- Installation: `npm install d3 @types/d3`

**Victory** (Alternative React charting):

- Good for animations
- Installation: `npm install victory`

### Data Table Libraries

#### Primary: TanStack Table (React Table v8)

**Why TanStack Table**:

- Headless (full control over UI)
- TypeScript-first
- Excellent performance (virtualization)
- Sorting, filtering, pagination built-in
- Server-side data support
- Column resizing, reordering
- Row selection
- Active development

**Installation**:

```bash
npm install @tanstack/react-table
```

**Features**:

- Client-side and server-side data
- Column sorting (multi-column)
- Column filtering (text, date, number)
- Pagination (client/server)
- Row selection
- Column visibility
- Column resizing
- Column reordering
- Export to CSV/Excel
- Virtual scrolling for large datasets

**Usage Example**:

```typescript
import { useReactTable, getCoreRowModel, getSortedRowModel, getFilteredRowModel } from '@tanstack/react-table';

export function DealsTable({ data }: { data: Deal[] }) {
  const columns = useMemo(() => [
    { accessorKey: 'symbol', header: 'Symbol' },
    { accessorKey: 'quantity', header: 'Quantity' },
    { accessorKey: 'price', header: 'Price' },
    { accessorKey: 'date', header: 'Date' },
  ], []);

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  });

  // Render table with full control over UI
}
```

#### Alternative: shadcn/ui DataTable

- Built on TanStack Table
- Pre-styled components
- Quick setup
- Installation: `npx shadcn-ui@latest add table`

### Form Libraries

#### Primary: React Hook Form

**Why React Hook Form**:

- Performance (minimal re-renders)
- Small bundle size
- TypeScript support
- Easy validation
- Great DX

**Installation**:

```bash
npm install react-hook-form
npm install @hookform/resolvers zod  # For Zod validation
```

**Features**:

- Uncontrolled components (better performance)
- Built-in validation
- Integration with Zod/Yup
- Error handling
- Field arrays
- Conditional fields
- Async validation

**Usage Example**:

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
      {/* ... */}
    </form>
  );
}
```

#### Validation: Zod

- TypeScript-first schema validation
- Type inference
- Great error messages
- Installation: `npm install zod`

### UI Component Libraries

#### Primary: shadcn/ui

**Why shadcn/ui**:

- Copy-paste components (not a dependency)
- Fully customizable
- Built on Radix UI (accessible)
- Tailwind CSS styling
- TypeScript support
- Active community

**Installation**:

```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
# ... add components as needed
```

**Available Components**:

- Button, Card, Dialog, Dropdown, Input, Select
- Table, Tabs, Toast, Tooltip, Form
- Accordion, Alert, Avatar, Badge, Calendar
- Checkbox, Radio, Switch, Slider, Progress
- And many more...

#### Base: Radix UI

- Accessible component primitives
- Unstyled (full style control)
- Used by shadcn/ui
- Installation: Individual packages (e.g., `@radix-ui/react-dialog`)

### State Management

#### Server State: TanStack Query (React Query)

**Why TanStack Query**:

- Server state management
- Caching and synchronization
- Background refetching
- Optimistic updates
- Great DevTools

**Installation**:

```bash
npm install @tanstack/react-query
```

**Features**:

- Automatic caching
- Background refetching
- Request deduplication
- Pagination support
- Infinite queries
- Mutations with optimistic updates
- DevTools for debugging

**Usage Example**:

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function DealsList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['deals'],
    queryFn: fetchDeals,
  });

  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: createDeal,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deals'] });
    },
  });

  // ...
}
```

#### Client State: Zustand (Lightweight)

**Why Zustand**:

- Simple API
- Small bundle size
- No providers needed
- TypeScript support
- DevTools support

**Installation**:

```bash
npm install zustand
```

**Use Cases**:

- Auth state
- UI state (modals, sidebars)
- User preferences
- Theme state

### API Client

#### Primary: Axios or Fetch API

**Axios** (Recommended):

- Request/response interceptors
- Automatic JSON parsing
- Request cancellation
- Better error handling
- Installation: `npm install axios`

**Fetch API** (Built-in):

- No dependencies
- Modern API
- Good for simple cases

**Custom API Client**:

```typescript
// lib/services/api.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth interceptor
apiClient.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
```

### Internationalization (i18n)

#### Primary: next-intl

**Why next-intl**:

- Built for Next.js App Router
- TypeScript support
- Server Components support
- Route-based localization
- Great performance

**Installation**:

```bash
npm install next-intl
```

**Features**:

- Server and client components
- Route-based locales
- Type-safe translations
- Pluralization
- Date/number formatting
- RTL support

### Date & Time Handling

#### Primary: date-fns

**Why date-fns**:

- Tree-shakeable (small bundle)
- Immutable
- TypeScript support
- Great API

**Installation**:

```bash
npm install date-fns
```

**Usage**:

```typescript
import { format, parseISO, differenceInDays } from 'date-fns';

format(new Date(), 'yyyy-MM-dd');
differenceInDays(date1, date2);
```

### File Upload

#### Primary: react-dropzone

**Why react-dropzone**:

- Drag and drop support
- File validation
- Preview support
- Accessible

**Installation**:

```bash
npm install react-dropzone
```

### Animation

#### Primary: Framer Motion

**Why Framer Motion**:

- Declarative animations
- Gesture support
- Layout animations
- Great performance

**Installation**:

```bash
npm install framer-motion
```

### Icon Libraries

#### Primary: Lucide React

**Why Lucide**:

- Large icon set
- Tree-shakeable
- Consistent design
- TypeScript support

**Installation**:

```bash
npm install lucide-react
```

### Utility Libraries

#### Type Utilities: TypeScript

- Built-in type utilities
- No additional library needed

#### Data Validation: Zod

- Already mentioned in forms
- Also useful for API validation

#### URL Handling: next/navigation

- Built into Next.js
- `useRouter`, `usePathname`, `useSearchParams`

### Development Tools

#### Type Checking: TypeScript

- Built-in compiler
- `tsc --noEmit` in CI/CD

#### Linting: ESLint

- Next.js ESLint config
- Custom rules
- Installation: Included with Next.js

#### Formatting: Prettier

- Code formatting
- Integration with ESLint
- Installation: `npm install -D prettier eslint-config-prettier`

#### Testing: Jest + React Testing Library

- Unit and integration tests
- Installation: `npm install -D jest @testing-library/react @testing-library/jest-dom`

#### E2E Testing: Playwright

- End-to-end testing
- Installation: `npm install -D @playwright/test`

### Package Management

#### Primary: npm or pnpm

- **npm**: Default with Node.js
- **pnpm**: Faster, disk-efficient (recommended)
- Installation: `npm install -g pnpm`
- Usage: `pnpm install`, `pnpm add <package>`

### Frontend Stack Summary

**Core**:

- Next.js 14+ (App Router)
- TypeScript (strict mode)
- Tailwind CSS
- React 18+

**Charts & Visualization**:

- Recharts (primary)
- Chart.js (optional)
- D3.js (advanced custom)

**Data Tables**:

- TanStack Table (primary)
- shadcn/ui DataTable (pre-styled option)

**Forms**:

- React Hook Form
- Zod (validation)

**UI Components**:

- shadcn/ui (primary)
- Radix UI (base primitives)

**State Management**:

- TanStack Query (server state)
- Zustand (client state)

**API Client**:

- Axios (recommended)
- Fetch API (built-in)

**i18n**:

- next-intl

**AI Integration**:

- **Vercel AI SDK Core** (`ai`): Unified API for text generation, structured objects, tool calls, agents
- Supports multiple providers (OpenAI, Anthropic, Google, etc.)
- Streaming support
- RAG support via Language Model Middleware
- Tool calling and function execution
- **Vercel AI SDK UI** (`@ai-sdk/react`): Framework-agnostic hooks for chat and generative UI
- `useChat`: Chat interface with streaming, history, tool usage
- `useCompletion`: Text completion interface
- `useObject`: Structured object generation
- Message persistence support
- Resume stream support

**Utilities**:

- date-fns (dates)
- react-dropzone (file upload)
- framer-motion (animations)
- lucide-react (icons)

**Development**:

- ESLint + Prettier
- Jest + React Testing Library
- Playwright (E2E)

### Installation Commands

**Application Website**:

```bash
# Core
npm create next-app@latest . --typescript --tailwind --app
npm install @tanstack/react-query @tanstack/react-table
npm install recharts
npm install react-hook-form @hookform/resolvers zod
npm install axios zustand
npm install next-intl
npm install date-fns
npm install react-dropzone framer-motion lucide-react

# AI SDK (Vercel AI SDK)
npm install ai @ai-sdk/openai @ai-sdk/anthropic  # Core + providers
npm install @ai-sdk/react  # AI SDK UI hooks (useChat, useCompletion, etc.)

# UI Components
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card dialog input select table

# Development
npm install -D @types/node @types/react @types/react-dom
npm install -D eslint-config-next prettier eslint-config-prettier
npm install -D jest @testing-library/react @testing-library/jest-dom
npm install -D @playwright/test
```

**Marketing Website**:

```bash
# Core (same as application)
npm create next-app@latest . --typescript --tailwind --app

# Content
npm install next-mdx-remote
npm install gray-matter  # For frontmatter parsing

# SEO
npm install next-seo  # For meta tags

# Analytics (optional)
npm install @vercel/analytics
```

### Technology Stack Validation

Before starting development, ensure:

- [ ] All core libraries installed
- [ ] Chart library tested with sample data
- [ ] Data table library tested with sample data
- [ ] Form library tested with validation
- [ ] UI components accessible
- [ ] State management working
- [ ] API client configured
- [ ] i18n setup and tested
- [ ] AI SDK installed and configured
- [ ] AI SDK UI hooks tested (useChat)
- [ ] Development tools configured
- [ ] AI SDK installed and configured
- [ ] AI SDK UI hooks tested (useChat)

---

## Vercel AI SDK Integration

### Overview

The [Vercel AI SDK](https://ai-sdk.dev/docs/introduction) provides a unified, framework-agnostic toolkit for building AI-powered applications. It standardizes AI model integration across multiple providers (OpenAI, Anthropic, Google, etc.) and provides powerful UI hooks for building chat interfaces and generative user interfaces.**Why Vercel AI SDK**:

- **Unified API**: Single API works with multiple providers (OpenAI, Anthropic, Google, etc.)
- **Streaming Support**: Built-in streaming for real-time responses
- **Framework Agnostic**: Works with React, Next.js, Vue, Svelte, and more
- **TypeScript First**: Full TypeScript support with type safety
- **RAG Support**: Language Model Middleware for Retrieval Augmented Generation
- **Tool Calling**: Built-in support for function calling and tool execution
- **UI Components**: Pre-built hooks for chat interfaces (`useChat`, `useCompletion`)
- **Active Development**: Maintained by Vercel, widely adopted

### AI SDK Libraries

#### 1. AI SDK Core (`ai`)

**Purpose**: Unified API for generating text, structured objects, tool calls, and building agents with LLMs.**Key Features**:

- **Text Generation**: `generateText()` for simple text generation
- **Streaming**: `streamText()` for streaming responses
- **Structured Data**: `generateObject()` for generating structured JSON objects
- **Tool Calling**: Built-in support for function calling and tool execution
- **Agents**: Build multi-step agents with workflow patterns
- **RAG**: Language Model Middleware for Retrieval Augmented Generation
- **Multiple Providers**: Support for OpenAI, Anthropic, Google, Azure, and more

**Installation**:

```bash
npm install ai @ai-sdk/openai @ai-sdk/anthropic
```

**Backend Usage Example** (Next.js API Route):

```typescript
// app/api/ai/chat/route.ts
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = await streamText({
    model: openai('gpt-4'),
    messages,
    system: 'You are a helpful assistant for analyzing NSE bulk deals data.',
  });

  return result.toDataStreamResponse();
}
```

**RAG Implementation Example**:

```typescript
import { streamText, tool } from 'ai';
import { openai } from '@ai-sdk/openai';
import { createRetrievalChain } from 'ai/rsc'; // RAG support

// Tool for querying bulk deals data
const queryBulkDeals = tool({
  description: 'Query bulk deals data from database',
  parameters: z.object({
    symbol: z.string(),
    dateRange: z.object({
      start: z.string(),
      end: z.string(),
    }),
  }),
  execute: async ({ symbol, dateRange }) => {
    // Query database for bulk deals
    const deals = await db.queryBulkDeals(symbol, dateRange);
    return deals;
  },
});

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = await streamText({
    model: openai('gpt-4'),
    messages,
    tools: {
      queryBulkDeals,
    },
  });

  return result.toDataStreamResponse();
}
```

#### 2. AI SDK UI (`@ai-sdk/react`)

**Purpose**: Framework-agnostic hooks for quickly building chat and generative user interfaces.**Key Hooks**:

- **`useChat`**: Complete chat interface with streaming, history, and tool usage
- **`useCompletion`**: Text completion interface
- **`useObject`**: Structured object generation with streaming
- **Message Persistence**: Built-in support for saving/loading chat history
- **Resume Streams**: Ability to resume interrupted streams

**Installation**:

```bash
npm install @ai-sdk/react
```

**Frontend Usage Example**:

```typescript
// components/AIChat.tsx
'use client';

import { useChat } from '@ai-sdk/react';

export function AIChat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/ai/chat',
    onError: (error) => {
      console.error('Chat error:', error);
    },
  });

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto">
        {messages.map((message) => (
          <div key={message.id} className={message.role}>
            <div>{message.content}</div>
            {message.toolInvocations && (
              <div>
                {message.toolInvocations.map((tool) => (
                  <div key={tool.toolCallId}>
                    Tool: {tool.toolName} - {tool.state}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Ask about bulk deals..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          Send
        </button>
      </form>
    </div>
  );
}
```

**Message Persistence Example**:

```typescript
import { useChat } from '@ai-sdk/react';

export function AIChatWithPersistence() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/ai/chat',
    id: 'bulk-deals-chat', // Unique ID for persistence
    onFinish: async (message) => {
      // Save message to database
      await saveMessageToDB(message);
    },
    initialMessages: [], // Load from database on mount
  });

  // Load chat history on mount
  useEffect(() => {
    loadChatHistory('bulk-deals-chat').then((history) => {
      // Set initial messages
    });
  }, []);

  // ... rest of component
}
```

### AI SDK Integration in Our Project

#### Use Case: NSE Bulk Deals AI Analyzer

**Backend Implementation** (`backend/app/user/routes/ai_analyzer.py`):

```python
from fastapi import APIRouter, Depends
from ai import stream_text
from ai_sdk.openai import openai

router = APIRouter()

@router.post("/ask")
async def ask_ai_question(
    question: str,
    user_id: str = Depends(get_current_user)
):
    # Build context from user's bulk deals data
    context = await build_rag_context(user_id)
    
    # Use AI SDK Core for streaming response
    result = await stream_text(
        model=openai("gpt-4"),
        prompt=f"Context: {context}\n\nQuestion: {question}",
        tools={
            "query_deals": query_bulk_deals_tool,
            "analyze_trends": analyze_trends_tool,
        }
    )
    
    return StreamingResponse(result.to_data_stream())
```

**Frontend Implementation** (`frontend/app/(user)/ai-analyzer/page.tsx`):

```typescript
'use client';

import { useChat } from '@ai-sdk/react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default function AIAnalyzerPage() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/user/ai/ask',
    id: 'nse-bulk-deals-analyzer',
    onFinish: async (message) => {
      // Save to database
      await fetch('/api/user/ai/history', {
        method: 'POST',
        body: JSON.stringify(message),
      });
    },
  });

  const suggestedQuestions = [
    "What are the top 10 bulk deals by quantity today?",
    "Show me all BUY deals for RELIANCE in the last week",
    "Which stocks have the highest accumulation this month?",
  ];

  return (
    <div className="container mx-auto p-6">
      <Card>
        <CardHeader>
          <CardTitle>AI Bulk Deals Analyzer</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Suggested Questions */}
            <div>
              <h3 className="text-sm font-medium mb-2">Suggested Questions:</h3>
              <div className="flex flex-wrap gap-2">
                {suggestedQuestions.map((question, idx) => (
                  <Button
                    key={idx}
                    variant="outline"
                    size="sm"
                    onClick={() => handleInputChange({ target: { value: question } } as any)}
                  >
                    {question}
                  </Button>
                ))}
              </div>
            </div>

            {/* Chat Messages */}
            <div className="border rounded-lg p-4 h-96 overflow-y-auto">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`mb-4 ${
                    message.role === 'user' ? 'text-right' : 'text-left'
                  }`}
                >
                  <div
                    className={`inline-block p-2 rounded ${
                      message.role === 'user'
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-200 text-gray-800'
                    }`}
                  >
                    {message.content}
                  </div>
                  {message.toolInvocations && (
                    <div className="mt-2 text-xs text-gray-500">
                      {message.toolInvocations.map((tool) => (
                        <div key={tool.toolCallId}>
                          Using tool: {tool.toolName}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
              {isLoading && (
                <div className="text-gray-500">Thinking...</div>
              )}
            </div>

            {/* Input Form */}
            <form onSubmit={handleSubmit} className="flex gap-2">
              <Input
                value={input}
                onChange={handleInputChange}
                placeholder="Ask about bulk deals data..."
                disabled={isLoading}
                className="flex-1"
              />
              <Button type="submit" disabled={isLoading}>
                Send
              </Button>
            </form>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
```

### RAG (Retrieval Augmented Generation) Implementation

**Context Building**:

```typescript
// lib/services/ai/rag-context.ts
import { db } from '@/lib/db';

export async function buildRAGContext(userId: string, question: string) {
  // Extract entities from question (symbols, dates, etc.)
  const entities = extractEntities(question);
  
  // Query relevant bulk deals data
  const deals = await db.queryBulkDeals({
    userId,
    symbols: entities.symbols,
    dateRange: entities.dateRange,
    limit: 50, // Top 50 most relevant deals
  });
  
  // Build context string
  const context = `
    User's Bulk Deals Data:
    ${deals.map(deal => 
      `${deal.symbol}: ${deal.quantity} @ ${deal.price} on ${deal.date}`
    ).join('\n')}
    
    User Question: ${question}
  `;
  
  return context;
}
```

### Tool Calling for Data Queries

**Define Tools**:

```typescript
// lib/services/ai/tools.ts
import { tool } from 'ai';
import { z } from 'zod';
import { db } from '@/lib/db';

export const queryBulkDealsTool = tool({
  description: 'Query bulk deals data from the database',
  parameters: z.object({
    symbol: z.string().optional(),
    dateRange: z.object({
      start: z.string(),
      end: z.string(),
    }).optional(),
    dealType: z.enum(['BUY', 'SELL']).optional(),
    limit: z.number().default(20),
  }),
  execute: async ({ symbol, dateRange, dealType, limit }) => {
    const deals = await db.queryBulkDeals({
      symbol,
      dateRange,
      dealType,
      limit,
    });
    return deals;
  },
});

export const analyzeTrendsTool = tool({
  description: 'Analyze trends in bulk deals data',
  parameters: z.object({
    symbol: z.string(),
    period: z.enum(['day', 'week', 'month']),
  }),
  execute: async ({ symbol, period }) => {
    const trends = await db.analyzeTrends(symbol, period);
    return trends;
  },
});
```

### Provider Configuration

**Environment Variables**:

```bash
# .env.local
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Optional: Use Vercel AI Gateway for unified access
VERCEL_AI_GATEWAY_API_KEY=your_gateway_key
```

**Provider Selection**:

```typescript
// lib/ai/config.ts
import { openai } from '@ai-sdk/openai';
import { anthropic } from '@ai-sdk/anthropic';

export function getAIModel(provider: 'openai' | 'anthropic' = 'openai') {
  switch (provider) {
    case 'openai':
      return openai('gpt-4');
    case 'anthropic':
      return anthropic('claude-sonnet-4.5');
    default:
      return openai('gpt-4');
  }
}
```

### Benefits for Our Project

1. **Unified API**: Switch between OpenAI, Anthropic, Google without code changes
2. **Streaming**: Real-time responses improve user experience
3. **RAG Support**: Easy integration with our bulk deals database
4. **Tool Calling**: Query database directly from AI responses
5. **Type Safety**: Full TypeScript support prevents errors
6. **UI Hooks**: `useChat` provides complete chat interface out of the box
7. **Message Persistence**: Built-in support for saving chat history
8. **Error Handling**: Robust error handling and retry logic
9. **Cost Optimization**: Can use cheaper models for simple queries
10. **Active Development**: Well-maintained by Vercel

### Integration Checklist

- [ ] Install AI SDK Core and UI packages
- [ ] Configure provider API keys
- [ ] Create AI API route with streaming support
- [ ] Implement RAG context building
- [ ] Define tools for data queries
- [ ] Create frontend chat component with `useChat`
- [ ] Implement message persistence
- [ ] Add error handling and retry logic
- [ ] Test with different providers
- [ ] Monitor API usage and costs

### AI SDK Cookbook Recipes

The [AI SDK Cookbook](https://ai-sdk.dev/cookbook) provides open-source recipes, guides, and templates for building AI-powered applications. Below are the most relevant recipes for our NSE Bulk Deals Analyzer project:

#### Essential Guides

1. **Build a RAG Agent** ([Guide](https://ai-sdk.dev/cookbook/rag-agent))

                                                - **Use Case**: Perfect for our RAG implementation with bulk deals data
                                                - **Key Features**: 
                                                                                - Retrieval Augmented Generation with database queries
                                                                                - Context building from user's bulk deals data
                                                                                - Semantic search for relevant deals
                                                - **Implementation**: Use this guide to build our RAG system that retrieves relevant bulk deals based on user questions

2. **Build a SQL Agent** ([Guide](https://ai-sdk.dev/cookbook/sql-agent))

                                                - **Use Case**: Similar pattern to our database query tools
                                                - **Key Features**:
                                                                                - Natural language to SQL conversion
                                                                                - Safe database querying
                                                                                - Result interpretation
                                                - **Implementation**: Adapt this pattern for querying our Supabase database with natural language

#### Key Recipes for Our Project

1. **Stream Text** ([Recipe](https://ai-sdk.dev/cookbook/stream-text))

                                                - **Use Case**: Real-time streaming responses in chat
                                                - **Implementation**: Use `streamText()` for streaming AI responses to users
                                                - **Benefits**: Better UX with real-time feedback

2. **Stream Text with Chat Prompt** ([Recipe](https://ai-sdk.dev/cookbook/stream-text-with-chat-prompt))

                                                - **Use Case**: Chat interface with conversation history
                                                - **Implementation**: Maintain conversation context across messages
                                                - **Benefits**: Context-aware responses based on previous messages

3. **Call Tools** ([Recipe](https://ai-sdk.dev/cookbook/call-tools))

                                                - **Use Case**: Query bulk deals data from database
                                                - **Implementation**: Define tools for `queryBulkDeals`, `analyzeTrends`, `getTopSymbols`
                                                - **Benefits**: AI can directly query our database to answer questions

4. **Call Tools in Multiple Steps** ([Recipe](https://ai-sdk.dev/cookbook/stream-text-multi-step))

                                                - **Use Case**: Complex queries requiring multiple database calls
                                                - **Implementation**: For questions like "Compare RELIANCE deals this week vs last week"
                                                - **Benefits**: Handle multi-step reasoning and data aggregation

5. **Generate Object** ([Recipe](https://ai-sdk.dev/cookbook/generate-object))

                                                - **Use Case**: Structured responses (e.g., formatted deal summaries)
                                                - **Implementation**: Generate structured JSON responses for deal analysis
                                                - **Benefits**: Type-safe structured data for frontend rendering

6. **Stream Object** ([Recipe](https://ai-sdk.dev/cookbook/stream-object))

                                                - **Use Case**: Streaming structured data generation
                                                - **Implementation**: Stream structured deal analysis as it's generated
                                                - **Benefits**: Real-time structured data updates

7. **Share useChat State Across Components** ([Recipe](https://ai-sdk.dev/cookbook/share-usechat-state))

                                                - **Use Case**: Share chat state between components (chat history, sidebar, etc.)
                                                - **Implementation**: Use context or state management to share `useChat` state
                                                - **Benefits**: Consistent chat state across UI components

8. **Markdown Chatbot with Memoization** ([Recipe](https://ai-sdk.dev/cookbook/markdown-chatbot-memoization))

                                                - **Use Case**: Chat interface with markdown rendering and caching
                                                - **Implementation**: Render markdown in responses and cache common queries
                                                - **Benefits**: Better formatting and performance optimization

9. **Caching Middleware** ([Recipe](https://ai-sdk.dev/cookbook/caching-middleware))

                                                - **Use Case**: Cache common queries to reduce API costs
                                                - **Implementation**: Cache frequent questions like "top deals today"
                                                - **Benefits**: Reduced API costs and faster responses

10. **Send Custom Body from useChat** ([Recipe](https://ai-sdk.dev/cookbook/send-custom-body))

                                                                - **Use Case**: Send additional context (user ID, filters, etc.) with chat requests
                                                                - **Implementation**: Include user context and preferences in API requests
                                                                - **Benefits**: Personalized responses based on user data

11. **Render Visual Interface in Chat** ([Recipe](https://ai-sdk.dev/cookbook/render-visual-interface))

                                                                - **Use Case**: Render charts and visualizations in chat responses
                                                                - **Implementation**: Generate and display charts for deal analysis
                                                                - **Benefits**: Rich visual responses for data analysis

12. **Human-in-the-Loop Agent** ([Recipe](https://ai-sdk.dev/cookbook/human-in-the-loop-agent))

                                                                - **Use Case**: Allow users to approve/refine AI actions
                                                                - **Implementation**: For sensitive operations like data exports
                                                                - **Benefits**: User control over AI actions

#### Templates to Reference

1. **Internal Knowledge Base (RAG)** ([Template](https://ai-sdk.dev/cookbook/internal-knowledge-base-rag))

                                                - **Use Case**: Similar to our bulk deals knowledge base
                                                - **Key Features**: RAG implementation with guardrails
                                                - **Implementation**: Reference this template for our RAG architecture

2. **Natural Language PostgreSQL** ([Template](https://ai-sdk.dev/cookbook/natural-language-postgres))

                                                - **Use Case**: Very similar to our use case - querying database with natural language
                                                - **Key Features**: Natural language to SQL conversion
                                                - **Implementation**: Adapt this pattern for Supabase/PostgreSQL queries

3. **Chatbot Starter Template** ([Template](https://ai-sdk.dev/cookbook/chatbot-starter))

                                                - **Use Case**: Complete chatbot implementation
                                                - **Key Features**: Persistence, multi-modal chat
                                                - **Implementation**: Use as reference for our chat interface

4. **Multi-Step Tools** ([Template](https://ai-sdk.dev/cookbook/multi-step-tools))

                                                - **Use Case**: Complex multi-step queries
                                                - **Key Features**: Automatic handling of multiple tool steps
                                                - **Implementation**: For complex analysis requiring multiple data queries

#### Implementation Strategy

**Phase 1: Basic Chat (Week 1)**

- Use "Stream Text with Chat Prompt" recipe
- Implement basic chat interface with `useChat`
- Reference "Chatbot Starter Template"

**Phase 2: Tool Integration (Week 2)**

- Use "Call Tools" recipe for database queries
- Implement `queryBulkDeals` tool
- Reference "Natural Language PostgreSQL" template

**Phase 3: RAG Implementation (Week 3)**

- Follow "Build a RAG Agent" guide
- Implement context building from bulk deals data
- Reference "Internal Knowledge Base (RAG)" template

**Phase 4: Advanced Features (Week 4)**

- Use "Call Tools in Multiple Steps" for complex queries
- Implement "Generate Object" for structured responses
- Add "Caching Middleware" for performance
- Use "Render Visual Interface" for charts

**Phase 5: Optimization (Week 5)**

- Implement "Markdown Chatbot with Memoization"
- Add "Share useChat State" for better state management
- Optimize with caching and error handling

#### Cookbook Integration Checklist

- [ ] Review "Build a RAG Agent" guide
- [ ] Study "Natural Language PostgreSQL" template
- [ ] Implement "Stream Text with Chat Prompt" recipe
- [ ] Create tools using "Call Tools" recipe
- [ ] Add multi-step support with "Call Tools in Multiple Steps"
- [ ] Implement structured responses with "Generate Object"
- [ ] Add caching with "Caching Middleware"
- [ ] Reference "Chatbot Starter Template" for UI
- [ ] Implement markdown rendering
- [ ] Add visual interface rendering for charts

### References

- [AI SDK Documentation](https://ai-sdk.dev/docs/introduction)
- [AI SDK Cookbook](https://ai-sdk.dev/cookbook) - Recipes, guides, and templates
- [AI SDK Core API](https://ai-sdk.dev/docs/reference/ai-sdk-core)
- [AI SDK UI Hooks](https://ai-sdk.dev/docs/reference/ai-sdk-ui)
- [RAG with AI SDK](https://ai-sdk.dev/docs/guides/provider-middleware/retrieval-augmented-generation)
- [Tool Calling](https://ai-sdk.dev/docs/guides/tools)
- [Build a RAG Agent Guide](https://ai-sdk.dev/cookbook/rag-agent)
- [Natural Language PostgreSQL Template](https://ai-sdk.dev/cookbook/natural-language-postgres)

---

## Git Worktree Setup for Parallel AI Agent Development

### Overview

**Git worktree** allows multiple working directories for the same repository, enabling parallel AI agents to work on different features simultaneously without conflicts. This is essential for the multi-agent delegation strategy.

### Why Git Worktree?

- **Parallel Development**: Multiple agents can work on different streams simultaneously
- **No Conflicts**: Each agent has its own working directory and branch
- **Isolated Changes**: Changes in one worktree don't affect others until merged
- **Efficient**: Share the same `.git` directory, so it's space-efficient
- **Safe**: Can test and develop features independently

### Setup Instructions

#### 1. Initial Repository Setup

```bash
# Ensure you're in the main repository
cd /home/pranay_p/Documents/MYPROJ/NSEPRod

# Create main branch if not exists
git checkout -b main  # or master, depending on your default branch
```

#### 2. Create Worktrees for Each Agent Stream

Based on the multi-agent delegation strategy, create worktrees for each parallel stream:

```bash
# Stream 2: Backend Core Module
git worktree add ../NSEPRod-stream2-core -b stream2-backend-core

# Stream 3: Backend Auth Module
git worktree add ../NSEPRod-stream3-auth -b stream3-backend-auth

# Stream 4: Backend User Module
git worktree add ../NSEPRod-stream4-user -b stream4-backend-user

# Stream 5: Backend Admin Module
git worktree add ../NSEPRod-stream5-admin -b stream5-backend-admin

# Stream 7: Frontend Auth Journey
git worktree add ../NSEPRod-stream7-fe-auth -b stream7-frontend-auth

# Stream 8: Frontend User Journey
git worktree add ../NSEPRod-stream8-fe-user -b stream8-frontend-user

# Stream 9: Frontend Admin Journey
git worktree add ../NSEPRod-stream9-fe-admin -b stream9-frontend-admin

# Stream 10: Frontend Charts & Visualization
git worktree add ../NSEPRod-stream10-charts -b stream10-frontend-charts

# Stream 11: Frontend AI Analyzer
git worktree add ../NSEPRod-stream11-ai -b stream11-frontend-ai
```

#### 3. Worktree Structure

After setup, you'll have:

```javascript
/home/pranay_p/Documents/MYPROJ/
├── NSEPRod/                    # Main worktree (main branch)
│   └── .git/                   # Shared git directory
├── NSEPRod-stream2-core/       # Backend Core worktree
├── NSEPRod-stream3-auth/       # Backend Auth worktree
├── NSEPRod-stream4-user/       # Backend User worktree
├── NSEPRod-stream5-admin/     # Backend Admin worktree
├── NSEPRod-stream7-fe-auth/    # Frontend Auth worktree
├── NSEPRod-stream8-fe-user/    # Frontend User worktree
├── NSEPRod-stream9-fe-admin/   # Frontend Admin worktree
├── NSEPRod-stream10-charts/    # Frontend Charts worktree
└── NSEPRod-stream11-ai/        # Frontend AI worktree
```

### Agent Workflow with Git Worktree

#### For Each Agent:

1. **Navigate to Worktree**:
   ```bash
         cd ../NSEPRod-stream2-core  # Example for Stream 2
   ```

2. **Create Feature Branch**:
   ```bash
         git checkout -b feature/core-module-base
   ```

3. **Work on Tasks**:

- Agent works on assigned tasks
- Commits changes to feature branch
- No conflicts with other agents

4. **Push and Create PR**:
   ```bash
         git push origin feature/core-module-base
         # Create PR from feature branch to main
   ```

5. **After Merge, Update Worktree**:
   ```bash
         git checkout main
         git pull origin main
         git branch -d feature/core-module-base  # Clean up merged branch
   ```


### Managing Worktrees

#### List All Worktrees:

```bash
git worktree list
```

#### Remove a Worktree:

```bash
# When stream is complete
git worktree remove ../NSEPRod-stream2-core
# Or use prune to remove all stale worktrees
git worktree prune
```

#### Update All Worktrees:

```bash
# After merging to main, update all worktrees
for worktree in ../NSEPRod-stream*; do
  cd "$worktree" && git checkout main && git pull origin main
done
```

### Best Practices

1. **One Worktree Per Stream**: Each agent stream gets its own worktree
2. **Feature Branches**: Work on feature branches, not directly on stream branches
3. **Regular Sync**: Pull latest main branch regularly to stay updated
4. **Clean Up**: Remove worktrees when streams are complete
5. **Shared Resources**: Core module and database schema changes need coordination
6. **Merge Strategy**: Use PRs to merge feature branches to main, then update all worktrees

### Integration with Multi-Agent Delegation

#### Stream Assignment with Worktrees:

- **Stream 1 (Infrastructure)**: Main worktree (sequential, must complete first)
- **Stream 2 (Backend Core)**: `NSEPRod-stream2-core` worktree
- **Stream 3 (Backend Auth)**: `NSEPRod-stream3-auth` worktree
- **Stream 4 (Backend User)**: `NSEPRod-stream4-user` worktree
- **Stream 5 (Backend Admin)**: `NSEPRod-stream5-admin` worktree
- **Stream 6 (Backend AI)**: Can use main worktree or create separate (sequential after Stream 4)
- **Stream 7 (Frontend Auth)**: `NSEPRod-stream7-fe-auth` worktree
- **Stream 8 (Frontend User)**: `NSEPRod-stream8-fe-user` worktree
- **Stream 9 (Frontend Admin)**: `NSEPRod-stream9-fe-admin` worktree
- **Stream 10 (Frontend Charts)**: `NSEPRod-stream10-charts` worktree
- **Stream 11 (Frontend AI)**: `NSEPRod-stream11-ai` worktree

### Troubleshooting

#### Worktree Already Exists:

```bash
# If worktree path already exists
git worktree add --force ../NSEPRod-stream2-core -b stream2-backend-core
```

#### Branch Already Exists:

```bash
# If branch already exists, checkout existing branch
git worktree add ../NSEPRod-stream2-core stream2-backend-core
```

#### Conflicts During Merge:

- Resolve conflicts in the worktree where the conflict occurs
- Use standard git conflict resolution
- Coordinate with other agents if shared resources are involved

### Documentation

Create a `WORKTREES.md` file in the repository root documenting:

- List of all active worktrees
- Which agent/stream is using each worktree
- Current status of each worktree
- Instructions for new team members

---

## Design System & Image Generation Setup

### Overview

Design system and image generation tools are primarily used for the **Marketing Website**, though design patterns can be shared with the Application Website for consistency. The marketing website requires extensive design work for landing pages, blog posts, case studies, and promotional materials.

### Dribbble Integration (Design Inspiration & System)

#### Use Cases:

- **A. Design Inspiration**: Research and reference Dribbble designs for marketing website UI/UX patterns
- **B. Dribbble API Integration**: Fetch design assets, color palettes, and component references (if API available)
- **C. Design System Reference**: Use Dribbble designs as reference for establishing marketing website design system patterns
- **D. Landing Page Design**: Specific landing page design inspiration and patterns for marketing website

#### Implementation:

**1. Design System Setup with Dribbble Inspiration** (`setup-design-system-dribbble`):**Sub-tasks**:

1. Research Dribbble for financial/analytics platform designs
2. Create design system documentation (`marketing-website/src/design-system/`)
3. Extract color palettes from Dribbble inspirations
4. Document typography patterns from references
5. Create component library structure based on Dribbble patterns
6. Setup design tokens (colors, spacing, typography, shadows)
7. Create Storybook or design system documentation site
8. Integrate Dribbble API (if available) for design asset fetching
9. Create design reference board with saved Dribbble shots
10. Document design decisions and inspirations

**Design System Structure** (Marketing Website):

```javascript
marketing-website/
├── src/design-system/
│   ├── tokens/
│   │   ├── colors.ts          # Color palette from Dribbble inspiration
│   │   ├── typography.ts      # Typography scale
│   │   ├── spacing.ts         # Spacing system
│   │   └── shadows.ts         # Shadow system
│   ├── components/
│   │   ├── Button/
│   │   ├── Card/
│   │   ├── Input/
│   │   └── ... (based on Dribbble patterns)
│   ├── layouts/
│   │   ├── LandingPage/
│   │   └── Blog/
│   └── docs/
│       └── dribbble-references.md  # Links to Dribbble inspirations
```

**2. Landing Page Design** (`marketing-landing-page`):**Sub-tasks**:

1. Research landing page designs on Dribbble for financial/analytics platforms
2. Create landing page component structure
3. Design hero section with Dribbble-inspired layout
4. Create features section with visual elements
5. Design testimonials/social proof section
6. Create CTA sections with compelling design
7. Integrate Nanobanana-generated graphics
8. Implement responsive design based on Dribbble patterns
9. Add animations and interactions
10. Test landing page performance

### Nanobanana Integration (Image Generation)

#### Use Cases:

- **A. Landing Page Graphics**: Generate hero images, illustrations, and background graphics
- **B. Custom Icons**: Generate platform-specific icons for features, navigation, and UI elements
- **C. Data Visualization Images**: Generate images for charts, graphs, and data representations
- **D. Marketing Assets**: Generate images for marketing materials, social media, and promotional content

#### Implementation:

**1. Image Generation Setup** (`setup-image-generation-nanobanana`):**Sub-tasks**:

1. Research Nanobanana API/documentation
2. Setup Nanobanana API client/configuration
3. Create image generation service (`frontend/src/lib/services/image-generation.ts`)
4. Setup image storage (local or CDN)
5. Create image generation utilities
6. Configure image optimization pipeline
7. Setup caching for generated images
8. Create image generation hooks/components
9. Document image generation patterns
10. Test image generation workflow

**2. Image Generation Service Structure**:

```typescript
// frontend/src/lib/services/image-generation.ts
export interface ImageGenerationConfig {
  type: 'landing-graphic' | 'icon' | 'data-visualization' | 'marketing';
  prompt: string;
  style?: string;
  dimensions?: { width: number; height: number };
}

export class ImageGenerationService {
  async generateLandingGraphic(prompt: string): Promise<string>
  async generateIcon(description: string, style: string): Promise<string>
  async generateDataVisualization(chartType: string, data: any): Promise<string>
  async generateMarketingAsset(campaign: string, format: string): Promise<string>
}
```

**3. Integration Points**:**Landing Page Graphics** (`marketing-landing-page`):

- Hero section background/illustration
- Feature section icons and graphics
- Testimonial section visuals
- CTA section graphics

**Custom Icons** (Throughout frontend):

- Navigation icons
- Feature icons
- Status indicators
- Action buttons icons

**Data Visualization Images** (Application Website - `fe-charts-components`):

- Chart background graphics
- Data representation illustrations
- Analytics dashboard visuals
- Report graphics

**Marketing Assets** (Marketing Website):

- Social media images
- Email campaign graphics
- Promotional banners
- Ad creatives

### Design Workflow

1. **Research Phase**:

- Browse Dribbble for design inspiration
- Save relevant shots to design board
- Extract design patterns and elements

2. **Design System Creation**:

- Document design tokens from Dribbble references
- Create component library based on patterns
- Establish design guidelines

3. **Image Generation**:

- Generate landing page graphics with Nanobanana
- Create custom icons for platform
- Generate data visualization images
- Create marketing assets as needed

4. **Integration**:

- Integrate generated images into components
- Apply design system to all pages
- Ensure consistency across platform

### Environment Variables

Add to `.env.example`:

```bash
# Nanobanana API Configuration
NANOBANANA_API_KEY=your_nanobanana_api_key
NANOBANANA_API_URL=https://api.nanobanana.com

# Dribbble API (if used)
DRIBBBLE_API_KEY=your_dribbble_api_key
DRIBBBLE_API_URL=https://api.dribbble.com/v2
```

### Best Practices

1. **Design System**:

- Maintain consistency with Dribbble-inspired patterns
- Document all design decisions
- Keep design system updated

2. **Image Generation**:

- Cache generated images to reduce API calls
- Optimize images for web (compression, formats)
- Use appropriate image formats (WebP, AVIF)
- Implement lazy loading for images

3. **Performance**:

- Pre-generate common images
- Use CDN for image delivery
- Implement image optimization pipeline

---

## MCP (Model Context Protocol) Server Integration

### Overview

MCP servers extend AI agent capabilities by providing access to external services, tools, and APIs. This enables agents to interact with browsers, databases, file systems, GitHub, and other services directly, making development more efficient and automated.

### MCP Servers for This Project

#### 1. Browser MCP Server (cursor-browser-extension)

**Purpose**: Web testing, scraping, and automation**Use Cases**:

- **Frontend Testing**: Automated browser testing of Next.js application
- **NSE Data Scraping**: Automated fetching of bulk deals data from NSE website
- **Visual Regression Testing**: Screenshot comparison for UI changes
- **E2E Testing**: End-to-end user flow testing
- **Network Monitoring**: Monitor API calls and responses
- **Console Debugging**: Access browser console logs

**Configuration**:

```json
{
  "mcpServers": {
    "cursor-browser-extension": {
      "command": "npx",
      "args": ["-y", "@cursor/browser-extension"]
    }
  }
}
```

**Integration Points**:

- NSE fetcher module: Use browser MCP to navigate NSE website and extract data
- Frontend testing: Automated testing of all user journeys
- Visual verification: Screenshot-based testing for UI components
- Network debugging: Monitor API calls during development

#### 2. GitHub MCP Server

**Purpose**: Repository management, CI/CD automation, PR management**Use Cases**:

- **CI/CD Automation**: Trigger workflows, check build status
- **PR Management**: Create PRs, review code, merge branches
- **Repository Operations**: File operations, branch management
- **Issue Tracking**: Create and manage GitHub issues
- **Release Management**: Create releases and tags

**Configuration**:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**Integration Points**:

- Git worktree management: Automate branch creation for worktrees
- CI/CD pipeline: Monitor and trigger deployments
- Code review: Automated PR creation and review
- Release automation: Tag releases and create changelogs

#### 3. File System MCP Server

**Purpose**: File operations, code generation, project management**Use Cases**:

- **Code Generation**: Generate files and modules based on templates
- **File Operations**: Read, write, search files across project
- **Project Structure**: Create directory structures
- **Code Refactoring**: Bulk file operations and refactoring
- **Template Generation**: Generate boilerplate code

**Configuration**:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "args": ["--allowed-directories", "/home/pranay_p/Documents/MYPROJ/NSEPRod"]
    }
  }
}
```

**Integration Points**:

- Module structure setup: Automate creation of module directories
- Code scaffolding: Generate component and route files
- Configuration files: Generate .env files, config files
- Documentation: Generate API docs, README files

#### 4. Database MCP Server (Supabase/PostgreSQL)

**Purpose**: Database operations, schema management, query execution**Use Cases**:

- **Schema Management**: Create and modify database schemas
- **Query Execution**: Run SQL queries for testing and debugging
- **Data Migration**: Execute and verify migrations
- **RLS Policy Testing**: Test Row Level Security policies
- **Data Seeding**: Seed test data for development

**Configuration**:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}"
      }
    }
  }
}
```

**Integration Points**:

- Database schema setup: Automate table creation and migrations
- RLS policy testing: Verify security policies
- Data validation: Test queries and data integrity
- Migration verification: Ensure migrations run correctly

#### 5. Testing MCP Server

**Purpose**: Automated testing, test generation, test execution**Use Cases**:

- **Test Generation**: Generate unit and integration tests
- **Test Execution**: Run test suites and report results
- **Coverage Analysis**: Check test coverage
- **E2E Test Automation**: Automate end-to-end tests
- **Performance Testing**: Run performance benchmarks

**Configuration**:

```json
{
  "mcpServers": {
    "testing": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-testing"]
    }
  }
}
```

**Integration Points**:

- Unit test generation: Auto-generate tests for new modules
- Test execution: Run tests in CI/CD pipeline
- Coverage tracking: Monitor test coverage across modules
- E2E automation: Automate user journey tests

### MCP Server Setup

#### 1. Installation

**Create MCP Configuration File** (`.cursor/mcp.json` or Cursor settings):

```json
{
  "mcpServers": {
    "cursor-browser-extension": {
      "command": "npx",
      "args": ["-y", "@cursor/browser-extension"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "--allowed-directories",
        "/home/pranay_p/Documents/MYPROJ/NSEPRod"
      ]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}"
      }
    }
  }
}
```

#### 2. Environment Variables

Add to `.env.example`:

```bash
# MCP Server Configuration
GITHUB_TOKEN=your_github_personal_access_token
DATABASE_URL=your_supabase_database_url
```

#### 3. MCP Server Usage in Development

**Browser MCP for NSE Data Fetching**:

```python
# Agent can use browser MCP to:
# 1. Navigate to NSE website
# 2. Extract bulk deals data
# 3. Handle dynamic content
# 4. Take screenshots for verification
```

**GitHub MCP for CI/CD**:

```python
# Agent can use GitHub MCP to:
# 1. Create feature branches
# 2. Create PRs after completing tasks
# 3. Check CI/CD status
# 4. Merge approved PRs
```

**File System MCP for Code Generation**:

```python
# Agent can use filesystem MCP to:
# 1. Generate module structure
# 2. Create component files
# 3. Generate API route files
# 4. Create configuration files
```

**Database MCP for Schema Management**:

```python
# Agent can use database MCP to:
# 1. Execute migrations
# 2. Test RLS policies
# 3. Verify data integrity
# 4. Seed test data
```

### MCP Server Integration with Work Streams

#### Stream 1 (Infrastructure):

- **File System MCP**: Generate project structure
- **Database MCP**: Setup and verify database schema
- **GitHub MCP**: Initialize repository and setup CI/CD

#### Stream 2 (Backend Core):

- **File System MCP**: Generate core module files
- **Database MCP**: Test database connections
- **Testing MCP**: Generate and run core module tests

#### Stream 3 (Backend Auth):

- **File System MCP**: Generate auth module structure
- **Database MCP**: Test auth-related queries
- **Testing MCP**: Generate auth tests

#### Stream 4 (Backend User):

- **File System MCP**: Generate user module files
- **Database MCP**: Test user data queries
- **Testing MCP**: Generate user module tests

#### Stream 5 (Backend Admin):

- **File System MCP**: Generate admin module files
- **Database MCP**: Test admin queries
- **Testing MCP**: Generate admin tests

#### Stream 6 (Backend AI):

- **File System MCP**: Generate AI service files
- **Testing MCP**: Generate AI service tests

#### Stream 7-11 (Frontend Streams):

- **Browser MCP**: Test frontend components and pages
- **File System MCP**: Generate frontend components
- **Testing MCP**: Generate frontend tests
- **Visual Testing**: Screenshot-based regression testing

### MCP Server Best Practices

1. **Security**:

- Store MCP server credentials in environment variables
- Use least privilege access for file system MCP
- Rotate API tokens regularly
- Never commit MCP credentials

2. **Performance**:

- Use MCP servers for repetitive tasks
- Cache results when possible
- Batch operations when applicable

3. **Error Handling**:

- Implement retry logic for MCP operations
- Handle MCP server failures gracefully
- Log MCP operations for debugging

4. **Testing**:

- Test MCP server integrations
- Verify MCP server availability
- Mock MCP servers in unit tests

### MCP Server Configuration File

Create `.cursor/mcp-config.json`:

```json
{
  "mcpServers": {
    "cursor-browser-extension": {
      "command": "npx",
      "args": ["-y", "@cursor/browser-extension"],
      "description": "Browser automation for testing and scraping"
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      },
      "description": "GitHub repository and CI/CD management"
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "--allowed-directories",
        "/home/pranay_p/Documents/MYPROJ/NSEPRod"
      ],
      "description": "File system operations and code generation"
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}"
      },
      "description": "Supabase/PostgreSQL database operations"
    }
  }
}
```

### MCP Server Documentation

Document MCP server usage in `docs/MCP_SERVERS.md`:

- List of configured MCP servers
- Use cases for each server
- Configuration instructions
- Examples of MCP server usage
- Troubleshooting guide

---

## Development Tools Setup

### Overview

Development tools enhance the local development experience by providing utilities for testing, debugging, and maintaining code quality. Based on the FastAPI full-stack template best practices, we include essential tools while keeping the setup simple and focused.

### Development Tools Included

#### 1. Mailcatcher (Email Testing)

**Purpose**: Catch and display all emails sent during development without sending real emails.**Why It's Essential**:

- Password reset emails need testing
- Welcome emails for new users
- Alert notifications via email (future)
- Email verification (if implemented)
- No risk of sending test emails to real users

**Setup**:

```bash
# Install Mailcatcher (Ruby gem)
gem install mailcatcher

# Or use Docker
docker run -d -p 1080:1080 -p 1025:1025 --name mailcatcher schickling/mailcatcher
```

**Configuration** (Backend `.env.development`):

```bash
# Email configuration for development
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USER=
SMTP_PASSWORD=
SMTP_TLS=false
```

**Usage**:

- Backend sends emails to `localhost:1025` (SMTP)
- View all emails at `http://localhost:1080` (Web UI)
- No real emails are sent during development

**Integration Points**:

- Password reset flow
- Welcome email on signup
- Alert notifications (future)
- Email verification (if implemented)

#### 2. Enhanced Pre-commit Hooks (Code Quality)

**Purpose**: Ensure code quality and consistency before commits.**Tools Included**:

- **Secret Detection**: detect-secrets, gitleaks, or truffleHog (already planned)
- **Python Linting**: ruff (fast, modern Python linter)
- **Python Formatting**: ruff format (or black)
- **TypeScript Linting**: ESLint with strict rules
- **TypeScript Formatting**: Prettier
- **Type Checking**: mypy (Python), tsc --noEmit (TypeScript)

**Setup** (Using prek - Rust-based, faster alternative to pre-commit):**Installation** (prek is a single binary, no Python/Node.js required):

```bash
# Download prek binary (Linux/macOS/Windows)
# Option 1: Using cargo (if Rust is installed)
cargo install prek

# Option 2: Download from GitHub releases
# Visit: https://github.com/j178/prek/releases
# Download appropriate binary for your OS

# Option 3: Using package managers
# macOS: brew install prek
# Linux: Download binary and add to PATH

# Verify installation
prek --version
```

**Initialize prek in repository**:

```bash
# Navigate to project root
cd /path/to/nse-bulk-deals-analyzer

# Install prek hooks (creates .git/hooks/pre-commit)
prek install

# Or for both application and marketing repos
# Application repo:
cd nse-bulk-deals-analyzer && prek install

# Marketing repo:
cd nse-bulk-deals-analyzer-marketing && prek install
```

**Configuration** (`.pre-commit-config.yaml`):

```yaml
repos:
  # Secret detection
 - repo: local
    hooks:
   - id: detect-secrets
        name: Detect secrets
        entry: detect-secrets scan --baseline .secrets.baseline
        language: system
        pass_filenames: false
        always_run: true

  # Python linting and formatting
 - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
   - id: ruff
        args: [--fix]
   - id: ruff-format

  # Python type checking
 - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
   - id: mypy
        additional_dependencies: [types-all]

  # TypeScript linting
 - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v9.0.0
    hooks:
   - id: eslint
        files: \.(ts|tsx|js|jsx)$
        types: [file]

  # TypeScript formatting
 - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
   - id: prettier
        files: \.(ts|tsx|js|jsx|json|md|css)$
```

**Usage**:

```bash
# Runs automatically before commit (via git hook)
git commit -m "Your message"

# Run manually on all files
prek run --all-files

# Run on specific files
prek run --files path/to/file.py path/to/file.ts

# Run hooks for files in specific directory
prek run --directory backend/app

# Run hooks for files changed in last commit
prek run --last-commit

# Run specific hooks
prek run ruff eslint

# List all configured hooks
prek list

# Update hook repositories
prek autoupdate

# Update with cooldown (mitigate supply chain attacks)
prek autoupdate --cooldown-days 7
```

**Benefits of prek over pre-commit**:

- Single binary, no Python/Node.js runtime required
- Faster execution (multiple times faster than pre-commit)
- Parallel hook execution
- Better disk space usage (shared toolchains)
- Built-in workspace/monorepo support
- Shell completions for easier hook selection
- Consistent code formatting
- Catch errors before commit
- Enforce code quality standards
- Prevent committing secrets
- Type checking before commit

#### 3. Optional Development Tools

**Adminer (Database Administration)**:

- **Purpose**: Web-based database administration tool
- **Why Optional**: Supabase provides a dashboard, but Adminer can be useful for local testing
- **Setup**: `docker run -d -p 8080:8080 --name adminer adminer`
- **Access**: `http://localhost:8080`
- **Use Case**: If you want to test with local PostgreSQL or need advanced SQL features

**Docker Compose (Optional)**:

- **Purpose**: Run entire stack locally with one command
- **Why Optional**: Since we use Supabase (remote), Next.js and FastAPI can run natively
- **When Useful**: For teams that prefer containerized development
- **Note**: Can be added later if needed, not essential for this project

**Traefik (Reverse Proxy - Optional)**:

- **Purpose**: Production-like routing with subdomains locally
- **Why Optional**: Simple port-based routing works fine for local development
- **When Useful**: Testing production-like setup with subdomains
- **Note**: Can be added for staging/production testing

### Development URLs

**Local Development URLs**:

- Frontend: `http://localhost:3000` (Next.js default)
- Backend API: `http://localhost:8000`
- API Documentation (Swagger): `http://localhost:8000/docs`
- API Documentation (ReDoc): `http://localhost:8000/redoc`
- Mailcatcher: `http://localhost:1080`
- Adminer (optional): `http://localhost:8080`

### Development Workflow

#### 1. Start Development Servers:

**Backend**:

```bash
cd backend
fastapi dev app/main.py
# Or with uvicorn
uvicorn app.main:app --reload
```

**Frontend**:

```bash
cd frontend
npm run dev
```

**Mailcatcher**:

```bash
# Start Mailcatcher
mailcatcher
# Or with Docker
docker start mailcatcher
```

#### 2. Development Process:

1. **Code Changes**: Make changes in your editor
2. **Auto-reload**: Both servers auto-reload on file changes
3. **Email Testing**: Check Mailcatcher at `http://localhost:1080` for emails
4. **Pre-commit**: Hooks run automatically before commit
5. **Manual Testing**: Use Cursor browser for visual testing

#### 3. Testing Email Functionality:

1. Trigger email action (e.g., password reset)
2. Check Mailcatcher web UI at `http://localhost:1080`
3. View email content, formatting, and links
4. Test email links (they point to localhost)
5. No real emails are sent

### Environment Configuration

**Backend `.env.development`**:

```bash
# Email configuration (Mailcatcher)
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USER=
SMTP_PASSWORD=
SMTP_TLS=false
SMTP_FROM_EMAIL=noreply@localhost

# Other development settings
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
```

**Frontend `.env.development`**:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
```

### Best Practices

1. **Email Testing**:

- Always use Mailcatcher in development
- Test all email templates
- Verify email links work correctly
- Check email formatting in different clients (via Mailcatcher)

2. **Pre-commit Hooks**:

- Fix linting errors before committing
- Let formatters fix formatting automatically
- Review type errors before committing
- Never skip hooks (use `--no-verify` only in emergencies)

3. **Development Servers**:

- Use hot reload for faster development
- Monitor console logs for errors
- Use Cursor browser for visual testing
- Keep Mailcatcher running during development

### Troubleshooting

#### Mailcatcher Not Receiving Emails:

- Check SMTP configuration in backend `.env`
- Verify Mailcatcher is running: `http://localhost:1080`
- Check backend logs for SMTP errors
- Ensure port 1025 is not blocked

#### Pre-commit Hooks Failing:

- Run hooks manually: `prek run --all-files`
- Fix errors shown in output
- Re-stage files after fixes: `git add .`
- Commit again

#### Development Servers Not Starting:

- Check if ports are already in use
- Verify environment variables are set
- Check logs for specific errors
- Ensure dependencies are installed

---

## Documentation Requirements

### Overview

Comprehensive documentation is essential for a full product. This section outlines all documentation that should be created and maintained throughout the project lifecycle.

### Documentation Structure

```javascript
docs/
├── api/                          # API Documentation
│   ├── openapi.yaml             # OpenAPI/Swagger specification
│   ├── endpoints.md             # Endpoint reference
│   └── examples/                # API usage examples
├── user/                         # User Documentation
│   ├── getting-started.md       # Getting started guide
│   ├── user-guide.md            # Complete user guide
│   ├── faq.md                   # Frequently asked questions
│   └── tutorials/               # Step-by-step tutorials
├── developer/                    # Developer Documentation
│   ├── setup.md                 # Development setup guide
│   ├── architecture.md          # Architecture overview
│   ├── contributing.md          # Contribution guidelines
│   ├── modules/                 # Module-specific docs
│   └── api-reference.md         # Internal API reference
├── operations/                   # Operations Documentation
│   ├── deployment.md            # Deployment guide
│   ├── monitoring.md            # Monitoring and alerting
│   ├── troubleshooting.md       # Troubleshooting guide
│   └── runbooks/                # Operational runbooks
├── security/                     # Security Documentation
│   ├── security-policy.md       # Security policy
│   ├── threat-model.md          # Threat model
│   └── incident-response.md     # Incident response plan
└── admin/                        # Admin Documentation
    ├── admin-guide.md           # Admin user guide
    └── system-management.md     # System management guide
```

### 1. API Documentation

#### OpenAPI/Swagger Specification

**Purpose**: Machine-readable API specification for all endpoints**Content**:

- All API endpoints with request/response schemas
- Authentication requirements
- Error responses and codes
- Request/response examples
- Rate limiting information

**Location**: `docs/api/openapi.yaml` or auto-generated from FastAPI**Maintenance**: Auto-generated from FastAPI code, manually enhanced with examples**Access**:

- Development: `http://localhost:8000/docs` (Swagger UI)
- Development: `http://localhost:8000/redoc` (ReDoc)
- Production: `https://api.yourdomain.com/docs`

#### API Endpoint Reference

**Purpose**: Human-readable API documentation**Content**:

- Endpoint descriptions
- Authentication methods
- Request/response formats
- Error handling
- Code examples in multiple languages
- Rate limits and quotas

**Location**: `docs/api/endpoints.md`**Format**: Markdown with code examples

#### API Usage Examples

**Purpose**: Practical examples for common use cases**Content**:

- Authentication flow examples
- CRUD operation examples
- Error handling examples
- Integration examples (cURL, Python, JavaScript, etc.)

**Location**: `docs/api/examples/`

### 2. User Documentation

#### Getting Started Guide

**Purpose**: Help new users get started quickly**Content**:

- Account creation
- First login
- Basic navigation
- Quick start tutorial
- Common first tasks

**Location**: `docs/user/getting-started.md`**Target Audience**: New users

#### User Guide

**Purpose**: Comprehensive guide for all user features**Content**:

- All features explained
- Step-by-step instructions
- Screenshots and diagrams
- Tips and best practices
- Troubleshooting common issues

**Location**: `docs/user/user-guide.md`**Sections**:

- Dashboard overview
- Viewing and filtering bulk deals
- Creating watchlists
- Setting up alerts
- Using AI Analyzer
- Managing subscriptions
- Referral system

#### FAQ

**Purpose**: Answer common user questions**Content**:

- Frequently asked questions
- Common issues and solutions
- Feature explanations
- Billing questions
- Technical questions

**Location**: `docs/user/faq.md`**Maintenance**: Updated based on user support tickets

#### Tutorials

**Purpose**: Step-by-step guides for specific tasks**Content**:

- How to track specific stocks
- How to set up alerts
- How to use AI Analyzer effectively
- How to export data
- Advanced analytics techniques

**Location**: `docs/user/tutorials/`

### 3. Developer Documentation

#### Development Setup Guide

**Purpose**: Help developers set up the development environment**Content**:

- Prerequisites
- Installation steps
- Environment setup
- Database setup
- Running the application
- Common issues

**Location**: `docs/developer/setup.md`**Reference**: Should match README.md but more detailed

#### Architecture Documentation

**Purpose**: Explain system architecture and design decisions**Content**:

- System architecture overview
- Module structure and responsibilities
- Data flow diagrams
- Technology choices and rationale
- Design patterns used
- Scalability considerations

**Location**: `docs/developer/architecture.md`**Format**: Markdown with Mermaid diagrams

#### Contributing Guidelines

**Purpose**: Guide for contributors**Content**:

- Code style guidelines
- Git workflow
- Pull request process
- Testing requirements
- Documentation requirements
- Code review process

**Location**: `docs/developer/contributing.md`

#### Module Documentation

**Purpose**: Document each module's purpose and usage**Content**:

- Module overview
- Public APIs
- Dependencies
- Usage examples
- Testing guidelines

**Location**: `docs/developer/modules/`**Files**:

- `core-module.md`
- `auth-module.md`
- `user-module.md`
- `admin-module.md`

#### Internal API Reference

**Purpose**: Document internal APIs and utilities**Content**:

- Core utilities
- Shared services
- Helper functions
- Type definitions

**Location**: `docs/developer/api-reference.md`

### 4. Operations Documentation

#### Deployment Guide

**Purpose**: Guide for deploying to different environments**Content**:

- Prerequisites
- Environment setup
- Deployment steps
- Post-deployment verification
- Rollback procedures
- Environment-specific configurations

**Location**: `docs/operations/deployment.md`**Sections**:

- Development deployment
- Staging deployment
- Production deployment
- Database migrations
- Zero-downtime deployment

#### Monitoring and Alerting

**Purpose**: Guide for monitoring the application**Content**:

- Monitoring setup
- Key metrics to monitor
- Alert configuration
- Dashboard setup
- Log aggregation
- Performance monitoring

**Location**: `docs/operations/monitoring.md`

#### Troubleshooting Guide

**Purpose**: Common issues and solutions**Content**:

- Common errors and fixes
- Performance issues
- Database issues
- API issues
- Frontend issues
- Escalation procedures

**Location**: `docs/operations/troubleshooting.md`

#### Operational Runbooks

**Purpose**: Step-by-step procedures for common operations**Content**:

- Database backup and restore
- User data export
- System maintenance
- Security incident response
- Disaster recovery

**Location**: `docs/operations/runbooks/`

### 5. Security Documentation

#### Security Policy

**Purpose**: Document security policies and procedures**Content**:

- Security principles
- Vulnerability reporting
- Security update process
- Access control policies
- Data protection policies

**Location**: `docs/security/security-policy.md`

#### Threat Model

**Purpose**: Document potential threats and mitigations**Content**:

- Threat identification
- Risk assessment
- Mitigation strategies
- Security controls

**Location**: `docs/security/threat-model.md`

#### Incident Response Plan

**Purpose**: Procedures for security incidents**Content**:

- Incident classification
- Response procedures
- Communication plan
- Recovery procedures
- Post-incident review

**Location**: `docs/security/incident-response.md`

### 6. Admin Documentation

#### Admin User Guide

**Purpose**: Guide for admin users**Content**:

- Admin dashboard overview
- User management
- Data management
- System settings
- Analytics and reporting

**Location**: `docs/admin/admin-guide.md`

#### System Management Guide

**Purpose**: Advanced system management**Content**:

- System configuration
- Feature flags
- Subscription plan management
- System maintenance
- Backup and recovery

**Location**: `docs/admin/system-management.md`

### 7. Additional Documentation

#### README.md

**Purpose**: Project overview and quick start**Content**:

- Project description
- Quick start guide
- Key features
- Technology stack
- Links to other documentation

**Location**: `README.md` (root)

#### CHANGELOG.md

**Purpose**: Track changes and releases**Content**:

- Version history
- New features
- Bug fixes
- Breaking changes
- Migration guides

**Location**: `CHANGELOG.md` (root)**Format**: Keep a Changelog format

#### LICENSE

**Purpose**: Project license**Location**: `LICENSE` (root)

#### CONTRIBUTORS.md

**Purpose**: List of contributors**Location**: `CONTRIBUTORS.md` (root)

### Documentation Maintenance

1. **Keep Documentation Updated**:

- Update docs when code changes
- Review docs in PR process
- Regular documentation audits

2. **Documentation as Code**:

- Store docs in repository
- Version control documentation
- Code review for documentation

3. **Documentation Tools**:

- Markdown for all docs
- Mermaid for diagrams
- Auto-generate API docs from code
- Use documentation generators if needed

---

## Credential Management Strategy

### Overview

Managing credentials securely across different environments, services, and team members is critical for security and development efficiency. This section outlines a comprehensive credential management strategy.

### Credential Categories

#### 1. Environment-Specific Credentials

**Development Environment**:

- Supabase development project credentials
- Local database credentials (if used)
- Development API keys (OpenAI, Stripe test mode)
- Development email service (Mailcatcher)
- Local JWT secrets

**Staging Environment**:

- Supabase staging project credentials
- Staging API keys
- Staging email service
- Staging payment gateway (Stripe test)
- Staging JWT secrets

**Production Environment**:

- Supabase production project credentials
- Production API keys
- Production email service (SendGrid, AWS SES, etc.)
- Production payment gateway (Stripe live)
- Production JWT secrets
- Production encryption keys

#### 2. Service-Specific Credentials

**Supabase**:

- Project URL
- Anon key (public, can be in frontend)
- Service role key (secret, backend only)
- Database connection string (if direct access needed)

**OpenAI/Anthropic**:

- API key
- Organization ID (if applicable)

**Stripe**:

- Publishable key (public, frontend)
- Secret key (secret, backend only)
- Webhook signing secret

**Email Service**:

- SMTP credentials
- API key (if using API-based service)

**Vercel**:

- Deployment tokens
- Environment variables

**GitHub**:

- Personal access tokens
- SSH keys
- OAuth app credentials

### Credential Storage Strategy

#### 1. Local Development

**Structure**:

```javascript
.env.local                    # Local overrides (gitignored)
.env.development              # Development defaults (gitignored)
.env.example                  # Template (committed)
```

**Setup Process**:

1. Copy `.env.example` to `.env.development`
2. Fill in actual values (never commit)
3. Use `.env.local` for personal overrides

**Backend**:

```bash
# .env.development (gitignored)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_dev_anon_key
SUPABASE_SERVICE_KEY=your_dev_service_key
JWT_SECRET=dev_jwt_secret_xxxxx
OPENAI_API_KEY=sk-dev-xxxxx
STRIPE_SECRET_KEY=sk_test_xxxxx
SMTP_HOST=localhost
SMTP_PORT=1025
```

**Frontend**:

```bash
# .env.development (gitignored)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_dev_anon_key
NEXT_PUBLIC_ENVIRONMENT=development
```

#### 2. Team Credential Sharing

**Option A: Password Manager (Recommended)**:

- Use 1Password, Bitwarden, or similar
- Create shared vault for team
- Store credentials with descriptions
- Rotate credentials regularly

**Option B: Encrypted Credential Store**:

- Use `sops` (Mozilla SOPS) for encrypted files
- Store encrypted `.env` files in repository
- Team members decrypt with their keys
- Example: `.env.development.encrypted`

**Option C: Credential Management Service**:

- Use AWS Secrets Manager, HashiCorp Vault, or similar
- Team members access via CLI or API
- Automatic rotation support
- Audit logging

**Recommended**: Use password manager for simplicity, encrypted files for version control

#### 3. CI/CD Credential Management

**GitHub Secrets**:

- Store all secrets in GitHub repository settings
- Separate secrets for each environment
- Use environment-specific secrets in workflows

**Vercel Environment Variables**:

- Store frontend secrets in Vercel dashboard
- Separate for Development, Preview, Production
- Use Vercel CLI for local sync (optional)

**Backend Platform Secrets**:

- Railway/Render/Fly.io: Use platform's secret management
- Store all backend secrets in platform dashboard
- Never hardcode in code or config files

### Credential Management Workflow

#### For New Team Members:

1. **Onboarding**:

- Add to password manager vault (if used)
- Share `.env.example` file
- Provide access to:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Supabase projects (dev, staging, prod)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - GitHub repository
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Vercel project
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Backend platform
- Share credential document (encrypted or secure channel)

2. **Setup**:

- Clone repository
- Copy `.env.example` to `.env.development`
- Get credentials from password manager
- Fill in `.env.development`
- Test connection to all services

#### For New Environments:

1. **Create Environment**:

- Create new Supabase project
- Generate new API keys
- Create new Stripe account (if needed)
- Generate new JWT secrets

2. **Store Credentials**:

- Add to password manager
- Update `.env.example` with new variable names
- Add to CI/CD secrets
- Document in credential management doc

#### For Credential Rotation:

1. **Rotation Process**:

- Generate new credentials
- Update in all locations (password manager, CI/CD, platforms)
- Update `.env` files for all team members
- Deploy with new credentials
- Verify everything works
- Revoke old credentials after verification period

2. **Rotation Schedule**:

- JWT secrets: Every 90 days
- API keys: Every 180 days
- Database passwords: Every 90 days
- Service account keys: Every 180 days

### Credential Documentation

#### Credential Inventory Document

**Location**: `docs/operations/credentials-inventory.md` (encrypted or access-controlled)**Content**:

- List of all credentials
- Where each credential is used
- Where each credential is stored
- Last rotation date
- Next rotation date
- Owner/contact for each credential

**Format**:

```markdown
## Supabase Development

- **Project URL**: https://xxxxx.supabase.co
- **Anon Key**: Stored in password manager, Vercel env vars
- **Service Key**: Stored in password manager, backend platform
- **Last Rotated**: 2024-01-15
- **Next Rotation**: 2024-04-15
- **Owner**: DevOps Team
```

#### Credential Access Log

**Purpose**: Track who accessed which credentials**Content**:

- Access timestamp
- User/team member
- Credential accessed
- Purpose/reason
- Environment

**Storage**: Maintain in secure location, review regularly

### Security Best Practices

1. **Never Commit Credentials**:

- Use `.gitignore` for all `.env` files
- Pre-commit hooks to detect secrets
- CI/CD scanning for secrets

2. **Use Least Privilege**:

- Give team members only credentials they need
- Use different credentials for different environments
- Rotate credentials when team members leave

3. **Encrypt Sensitive Documentation**:

- Encrypt credential inventory
- Use secure channels for sharing
- Limit access to credential docs

4. **Monitor Credential Usage**:

- Log credential access
- Monitor for unusual patterns
- Alert on credential exposure

5. **Regular Audits**:

- Review credential access quarterly
- Verify all credentials are still needed
- Check for unused credentials
- Ensure rotation schedule is followed

### Credential Management Tools

#### Recommended Tools:

1. **1Password/Bitwarden**:

- Shared vaults for teams
- Secure credential sharing
- Access control
- Audit logs

2. **Mozilla SOPS**:

- Encrypt files in repository
- Version control encrypted files
- Team access via keys

3. **HashiCorp Vault**:

- Enterprise credential management
- Automatic rotation
- Fine-grained access control

4. **AWS Secrets Manager / Azure Key Vault**:

- Cloud-native solution
- Automatic rotation
- Integration with CI/CD

### Environment Variable Template

**Location**: `.env.example` (committed to repository)**Content**:

```bash
# ============================================
# Environment Configuration
# ============================================
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

# ============================================
# Supabase Configuration
# ============================================
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key
DATABASE_URL=postgresql://user:password@host:port/dbname

# ============================================
# Authentication Configuration
# ============================================
JWT_SECRET=your_jwt_secret_key_min_32_chars
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# ============================================
# AI Service Configuration
# ============================================
OPENAI_API_KEY=sk-your_openai_api_key
# OR
ANTHROPIC_API_KEY=sk-ant-your_anthropic_api_key

# ============================================
# Payment Gateway Configuration
# ============================================
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# ============================================
# Email Configuration
# ============================================
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USER=
SMTP_PASSWORD=
SMTP_TLS=false
SMTP_FROM_EMAIL=noreply@yourdomain.com

# ============================================
# CORS Configuration
# ============================================
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# ============================================
# Security Configuration
# ============================================
RATE_LIMIT_PER_USER=60
RATE_LIMIT_PER_IP=100
ACCOUNT_LOCKOUT_THRESHOLD=5
ACCOUNT_LOCKOUT_DURATION_MINUTES=15
PASSWORD_MIN_LENGTH=12
SESSION_TIMEOUT_MINUTES=30

# ============================================
# Encryption Configuration
# ============================================
ENCRYPTION_KEY=your_32_byte_base64_encoded_key
CSRF_SECRET=your_csrf_secret_key

# ============================================
# Monitoring & Logging
# ============================================
SENTRY_DSN=your_sentry_dsn_optional
LOG_LEVEL=DEBUG

# ============================================
# Frontend Environment Variables (Next.js)
# ============================================
# These are prefixed with NEXT_PUBLIC_ to be available in browser
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_ENVIRONMENT=development
NEXT_PUBLIC_SENTRY_DSN=your_sentry_dsn_optional
NEXT_PUBLIC_APP_VERSION=1.0.0

# Server-only variables (not exposed to client)
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_key
```

### Credential Rotation Checklist

**Before Rotation**:

- [ ] Identify all credentials to rotate
- [ ] Generate new credentials
- [ ] Document new credentials securely
- [ ] Notify team of rotation schedule

**During Rotation**:

- [ ] Update password manager
- [ ] Update CI/CD secrets
- [ ] Update platform secrets
- [ ] Update team `.env` files
- [ ] Deploy with new credentials
- [ ] Verify all services work

**After Rotation**:

- [ ] Monitor for errors
- [ ] Verify old credentials are revoked
- [ ] Update rotation dates
- [ ] Document rotation completion

---

## API Versioning & Migration Strategy

### Overview

API versioning ensures backward compatibility and allows gradual migration of clients to new API versions. This section outlines the versioning strategy and migration process.

### API Versioning Strategy

#### Versioning Approach: URL Path Versioning

**Format**: `/api/v{version}/{endpoint}`**Examples**:

- `GET /api/v1/user/deals`
- `POST /api/v2/user/deals`
- `GET /api/v1/auth/profile`

**Benefits**:

- Clear version in URL
- Easy to route to different versions
- Can run multiple versions simultaneously
- Easy to deprecate old versions

#### Version Numbering

- **Major Version (v1, v2)**: Breaking changes
- **Minor Version (v1.1, v1.2)**: New features, backward compatible
- **Patch**: Bug fixes (not exposed in URL)

### API Version Implementation

#### FastAPI Route Structure

```python
# backend/app/main.py
from fastapi import FastAPI
from app.api.v1 import router as v1_router
from app.api.v2 import router as v2_router

app = FastAPI()

# Version 1 routes
app.include_router(v1_router, prefix="/api/v1", tags=["v1"])

# Version 2 routes (when needed)
app.include_router(v2_router, prefix="/api/v2", tags=["v2"])
```

#### Version-Specific Routers

```javascript
backend/app/api/
├── v1/
│   ├── __init__.py
│   ├── auth.py
│   ├── user.py
│   └── admin.py
└── v2/
    ├── __init__.py
    ├── auth.py
    ├── user.py
    └── admin.py
```

### Breaking Changes Policy

#### What Constitutes Breaking Changes:

1. **Removing endpoints**
2. **Changing request/response structure** (removing required fields, changing field types)
3. **Changing authentication requirements**
4. **Changing error response format**
5. **Removing query parameters**
6. **Changing HTTP methods**

#### Non-Breaking Changes:

1. **Adding new endpoints**
2. **Adding optional fields to requests/responses**
3. **Adding new query parameters**
4. **Improving error messages**
5. **Performance improvements**

### API Migration Process

#### 1. Planning Phase

**Before Making Breaking Changes**:

- Identify all breaking changes
- Document impact on clients
- Plan migration path
- Set deprecation timeline

#### 2. Implementation Phase

**Create New Version**:

1. Create new version directory (`v2/`)
2. Copy existing routes to new version
3. Implement changes in new version
4. Keep old version functional
5. Update tests for both versions

**Example**:

```python
# v1/user/deals.py (existing)
@router.get("/deals")
async def get_deals_v1(filters: DealFiltersV1):
    # Old implementation
    pass

# v2/user/deals.py (new)
@router.get("/deals")
async def get_deals_v2(filters: DealFiltersV2):
    # New implementation with changes
    pass
```

#### 3. Deprecation Phase

**Deprecation Timeline**:

- **Announcement**: 3 months before deprecation
- **Deprecation Period**: 6 months (old version still works)
- **Removal**: After 6 months, remove old version

**Deprecation Headers**:

```python
from fastapi import Response

@router.get("/deals", deprecated=True)
async def get_deals_v1(response: Response):
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = "Sat, 31 Dec 2024 23:59:59 GMT"
    response.headers["Link"] = '</api/v2/user/deals>; rel="successor-version"'
    # Implementation
```

#### 4. Client Migration

**Migration Guide**:

- Document changes between versions
- Provide migration examples
- Update API documentation
- Notify API consumers

**Migration Support**:

- Run both versions during migration period
- Provide migration tools if needed
- Support clients during migration

### API Versioning Best Practices

1. **Version from Day One**:

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Start with `/api/v1/` from the beginning
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Don't wait until you need versioning

2. **Document Versions**:

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Document each version in OpenAPI spec
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Maintain changelog for each version
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Document breaking changes clearly

3. **Test Both Versions**:

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Write tests for all versions
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Ensure backward compatibility
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Test migration paths

4. **Monitor Usage**:

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Track which versions are used
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Monitor deprecation warnings
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Plan removal based on usage

5. **Communication**:

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Announce deprecations early
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Provide clear migration guides
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Support clients during migration

### API Migration Checklist

**Before Creating New Version**:

- [ ] Identify all breaking changes
- [ ] Document impact assessment
- [ ] Plan migration timeline
- [ ] Create migration guide
- [ ] Update API documentation

**During Implementation**:

- [ ] Create new version directory
- [ ] Implement new version
- [ ] Keep old version functional
- [ ] Write tests for both versions
- [ ] Update OpenAPI specification

**During Deprecation**:

- [ ] Add deprecation headers
- [ ] Announce deprecation (3 months notice)
- [ ] Monitor usage of old version
- [ ] Support client migrations
- [ ] Update documentation

**After Migration Period**:

- [ ] Verify all clients migrated
- [ ] Remove deprecated version
- [ ] Update documentation
- [ ] Archive old version code

---

## Database Migration Strategy

### Overview

Database migrations manage schema changes safely and consistently across environments. This section outlines the migration strategy using Supabase migrations.

### Migration Tool: Supabase Migrations

**Tool**: Supabase CLI with SQL migration files**Location**: `supabase/migrations/`**Format**: `{timestamp}_{description}.sql`**Example**: `20240115120000_create_user_profiles.sql`

### Migration File Structure

```javascript
supabase/
├── migrations/
│   ├── 20240115120000_initial_schema.sql
│   ├── 20240120140000_add_subscription_tables.sql
│   ├── 20240125160000_add_security_tables.sql
│   └── 20240201100000_add_indexes.sql
├── seed.sql                    # Seed data (optional)
└── config.toml                 # Supabase config
```

### Migration Workflow

#### 1. Create Migration

**Using Supabase CLI**:

```bash
# Create new migration
supabase migration new add_user_preferences

# This creates: supabase/migrations/20240115120000_add_user_preferences.sql
```

**Manual Creation**:

```bash
# Create file with timestamp
touch supabase/migrations/$(date +%Y%m%d%H%M%S)_add_user_preferences.sql
```

#### 2. Write Migration SQL

**Migration File Template**:

```sql
-- Migration: Add user preferences table
-- Created: 2024-01-15
-- Author: Developer Name
-- Description: Adds user_preferences table for storing user settings

-- Create table
CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    preference_key TEXT NOT NULL,
    preference_value JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, preference_key)
);

-- Create indexes
CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);
CREATE INDEX idx_user_preferences_key ON user_preferences(preference_key);

-- Setup RLS
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own preferences"
    ON user_preferences FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own preferences"
    ON user_preferences FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own preferences"
    ON user_preferences FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own preferences"
    ON user_preferences FOR DELETE
    USING (auth.uid() = user_id);

-- Add comment
COMMENT ON TABLE user_preferences IS 'User preferences and settings';
```

#### 3. Test Migration Locally

**Using Supabase Local Development**:

```bash
# Start local Supabase
supabase start

# Apply migration
supabase db reset  # Resets and applies all migrations

# Or apply specific migration
supabase migration up
```

#### 4. Review Migration

**Before Applying**:

- [ ] Review SQL for correctness
- [ ] Check for potential data loss
- [ ] Verify indexes are created
- [ ] Verify RLS policies are correct
- [ ] Test rollback if needed

#### 5. Apply to Staging

**Apply Migration**:

```bash
# Link to staging project
supabase link --project-ref your-staging-ref

# Apply migrations
supabase db push

# Or apply specific migration
supabase migration up
```

**Verify**:

- [ ] Check migration applied successfully
- [ ] Verify schema changes
- [ ] Test application functionality
- [ ] Check for errors in logs

#### 6. Apply to Production

**Production Migration Process**:

1. **Backup Database**: Create backup before migration
2. **Apply Migration**: Use Supabase dashboard or CLI
3. **Verify**: Check migration status
4. **Monitor**: Monitor for errors
5. **Rollback Plan**: Have rollback migration ready

**Using Supabase Dashboard**:

- Go to Database → Migrations
- Upload migration file
- Review and apply

**Using Supabase CLI**:

```bash
# Link to production project
supabase link --project-ref your-production-ref

# Apply migrations (with confirmation)
supabase db push --confirm
```

### Migration Best Practices

#### 1. Always Use Transactions

**Good**:

```sql
BEGIN;

CREATE TABLE new_table (...);
ALTER TABLE existing_table ADD COLUMN new_column TEXT;
CREATE INDEX idx_new_column ON existing_table(new_column);

COMMIT;
```

**Bad**:

```sql
-- No transaction - partial failure risk
CREATE TABLE new_table (...);
ALTER TABLE existing_table ADD COLUMN new_column TEXT;
```

#### 2. Make Migrations Reversible

**Create Rollback Migration**:

```sql
-- Rollback: Remove user_preferences table
-- Migration: 20240115120000_add_user_preferences.sql

DROP TABLE IF EXISTS user_preferences CASCADE;
```

**Or Include Rollback in Same File**:

```sql
-- Migration
CREATE TABLE user_preferences (...);

-- Rollback (commented, for reference)
-- DROP TABLE IF EXISTS user_preferences CASCADE;
```

#### 3. Test Migrations

**Test Checklist**:

- [ ] Test on local database
- [ ] Test with sample data
- [ ] Test rollback procedure
- [ ] Test on staging before production
- [ ] Verify RLS policies work correctly

#### 4. Handle Data Migrations

**Data Migration Example**:

```sql
-- Migration: Add new column with default, then backfill
BEGIN;

-- Add column with default
ALTER TABLE user_profiles 
ADD COLUMN subscription_tier TEXT DEFAULT 'free';

-- Backfill existing data
UPDATE user_profiles 
SET subscription_tier = 'free' 
WHERE subscription_tier IS NULL;

-- Make column NOT NULL after backfill
ALTER TABLE user_profiles 
ALTER COLUMN subscription_tier SET NOT NULL;

COMMIT;
```

#### 5. Index Creation Strategy

**Create Indexes Concurrently** (for large tables):

```sql
-- For large tables, use CONCURRENTLY
CREATE INDEX CONCURRENTLY idx_bulk_deals_date 
ON bulk_deals(deal_date);
```

**Note**: CONCURRENTLY requires separate transaction

### Migration Testing

#### 1. Local Testing

```bash
# Reset local database and apply all migrations
supabase db reset

# Test application with new schema
# Run tests
pytest

# Verify data integrity
```

#### 2. Staging Testing

```bash
# Apply migration to staging
supabase db push

# Run integration tests
# Verify application works
# Check performance
```

#### 3. Production Testing

- Apply during low-traffic period
- Monitor application logs
- Check database performance
- Verify no errors

### Rollback Strategy

#### 1. Create Rollback Migration

**Rollback File**:

```sql
-- Rollback: 20240115120000_add_user_preferences_rollback.sql

BEGIN;

-- Drop RLS policies
DROP POLICY IF EXISTS "Users can view own preferences" ON user_preferences;
DROP POLICY IF EXISTS "Users can insert own preferences" ON user_preferences;
DROP POLICY IF EXISTS "Users can update own preferences" ON user_preferences;
DROP POLICY IF EXISTS "Users can delete own preferences" ON user_preferences;

-- Drop indexes
DROP INDEX IF EXISTS idx_user_preferences_user_id;
DROP INDEX IF EXISTS idx_user_preferences_key;

-- Drop table
DROP TABLE IF EXISTS user_preferences CASCADE;

COMMIT;
```

#### 2. Test Rollback

```bash
# Test rollback on local/staging first
supabase migration down
# Or apply rollback migration
```

#### 3. Production Rollback

- Only if critical issue
- Have rollback migration ready
- Test rollback on staging first
- Backup before rollback
- Monitor after rollback

### Migration Naming Convention

**Format**: `{YYYYMMDDHHMMSS}_{description}.sql`**Examples**:

- `20240115120000_initial_schema.sql`
- `20240120140000_add_subscription_tables.sql`
- `20240125160000_add_security_audit_logs.sql`
- `20240201100000_add_indexes_for_performance.sql`
- `20240205120000_migrate_user_data.sql`

**Description Guidelines**:

- Use lowercase with underscores
- Be descriptive but concise
- Include action verb (add, create, modify, remove)
- Include entity name

### Migration Checklist

**Before Creating Migration**:

- [ ] Review schema changes needed
- [ ] Check for breaking changes
- [ ] Plan data migration if needed
- [ ] Consider rollback strategy

**When Writing Migration**:

- [ ] Use transactions
- [ ] Include indexes
- [ ] Add RLS policies
- [ ] Add comments
- [ ] Test locally

**Before Applying to Staging**:

- [ ] Review migration SQL
- [ ] Test on local database
- [ ] Verify rollback works
- [ ] Update documentation

**Before Applying to Production**:

- [ ] Test on staging
- [ ] Create database backup
- [ ] Have rollback ready
- [ ] Schedule during low traffic
- [ ] Notify team

**After Applying**:

- [ ] Verify migration success
- [ ] Test application
- [ ] Monitor for errors
- [ ] Update documentation
- [ ] Archive migration files

---

## Development Rules & Practices Files

### Overview

Each module should have its own development rules and practices file to ensure consistency, quality, and maintainability. These files document module-specific patterns, standards, and guidelines.

### Module Rules File Structure

Each module should have a `RULES.md` or `DEVELOPMENT.md` file:

```javascript
backend/app/
├── core/
│   └── RULES.md                 # Core module rules
├── auth/
│   └── RULES.md                 # Auth module rules
├── user/
│   └── RULES.md                 # User module rules
├── admin/
│   └── RULES.md                 # Admin module rules
└── shared/
    └── RULES.md                 # Shared module rules

frontend/src/
├── lib/
│   └── RULES.md                 # Core/lib rules
├── modules/
│   ├── auth/
│   │   └── RULES.md             # Auth module rules
│   ├── user/
│   │   └── RULES.md             # User module rules
│   └── admin/
│       └── RULES.md             # Admin module rules
└── components/
    └── RULES.md                 # Shared components rules
```

### Core Module Rules (`backend/app/core/RULES.md`)

**Content**:

- **Purpose**: Core utilities, database, security, NSE fetching
- **Dependencies**: None (foundation module)
- **Coding Standards**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - All functions must have type hints
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - All functions must have docstrings
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Use async/await for I/O operations
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Handle all exceptions
- **Database Patterns**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Always use parameterized queries
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Use connection pooling
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Implement retry logic for transient errors
- **Security Patterns**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Never log sensitive data
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Use encryption for sensitive operations
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Validate all inputs
- **Testing Requirements**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - 90% code coverage minimum
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Mock external dependencies
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Test error cases
- **Examples**:
  ```python
    # Good: Type hints, docstring, error handling
    async def get_bulk_deals(filters: dict) -> List[BulkDeal]:
        """
        Fetch bulk deals from database with filters.
        
        Args:
            filters: Dictionary of filter criteria
            
        Returns:
            List of BulkDeal objects
            
        Raises:
            DatabaseError: If database query fails
        """
        try:
            # Implementation
        except Exception as e:
            logger.error(f"Error fetching bulk deals: {e}")
            raise DatabaseError("Failed to fetch bulk deals") from e
  ```


### Auth Module Rules (`backend/app/auth/RULES.md`)

**Content**:

- **Purpose**: Authentication, authorization, user management
- **Dependencies**: core module
- **Security Requirements**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Never store passwords in plain text
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Use bcrypt with 12+ rounds
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Implement account lockout
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Log all authentication attempts
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Use secure session management
- **JWT Patterns**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Short-lived access tokens (30 min)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Longer refresh tokens (7 days)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Implement token blacklist
- **Password Policy**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Minimum 12 characters
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Require uppercase, lowercase, numbers, special chars
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Check password history
- **Testing Requirements**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Test all authentication flows
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Test security edge cases
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Test password policy enforcement
- **Examples**:
  ```python
    # Good: Secure password hashing
    def hash_password(password: str) -> str:
        """Hash password using bcrypt."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()
    
    # Good: Account lockout check
    async def check_account_lockout(user_id: UUID) -> bool:
        """Check if account is locked."""
        user = await get_user(user_id)
        if user.account_locked_until and user.account_locked_until > datetime.now():
            raise AccountLockedError("Account is locked")
        return False
  ```


### User Module Rules (`backend/app/user/RULES.md`)

**Content**:

- **Purpose**: User-facing features (deals, analytics, watchlists, alerts)
- **Dependencies**: core, auth modules
- **Data Access Patterns**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Always use RLS policies (don't bypass)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Filter by user_id in all queries
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Use pagination for large datasets
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Implement proper error handling
- **Subscription Gating**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Check subscription tier before feature access
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Return clear error messages for locked features
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Track feature usage
- **Testing Requirements**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Test with different subscription tiers
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Test RLS policies
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Test feature gating
- **Examples**:
  ```python
    # Good: RLS-aware query with user filtering
    async def get_user_deals(user_id: UUID, filters: dict) -> List[BulkDeal]:
        """Get deals for user (RLS ensures isolation)."""
        query = select(BulkDeal).where(
            BulkDeal.user_id == user_id,  # Explicit user filter
            # Additional filters
        )
        return await db.execute(query)
    
    # Good: Feature gating
    async def check_feature_access(user_id: UUID, feature: str) -> bool:
        """Check if user has access to feature."""
        subscription = await get_user_subscription(user_id)
        return subscription.plan.features.get(feature, False)
  ```


### Admin Module Rules (`backend/app/admin/RULES.md`)

**Content**:

- **Purpose**: Admin features, system management
- **Dependencies**: core, auth modules
- **Admin Access Patterns**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Always verify admin role
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Log all admin actions
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Use admin override for RLS when needed
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Implement audit trail
- **Security Requirements**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - MFA required for admin accounts
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Separate admin authentication flow
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Rate limit admin endpoints more strictly
- **Testing Requirements**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Test admin-only access
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Test non-admin access (should fail)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Test audit logging
- **Examples**:
  ```python
    # Good: Admin role check with audit log
    @router.get("/admin/users")
    async def get_all_users(admin: User = Depends(require_admin)):
        """Get all users (admin only)."""
        audit_logger.log_admin_action(
            admin_id=admin.id,
            action="view_all_users",
            details={}
        )
        return await get_all_users_from_db()
  ```


### Frontend Module Rules (`frontend/src/modules/*/RULES.md`)

**Content**:

- **Purpose**: Frontend module-specific patterns
- **Next.js Patterns**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Use Server Components by default
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Use Client Components only when needed (`'use client'`)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Fetch data in Server Components
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Use React hooks for client-side state
- **Component Patterns**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - One component per file
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Use TypeScript for all components
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Export default for pages, named exports for components
- **Testing Requirements**:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Test Server Components separately
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Test Client Components with React Testing Library
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Test user interactions
- **Examples**:
  ```typescript
    // Good: Server Component (default)
    export default async function DealsPage() {
      const deals = await getDeals(); // Server-side data fetching
      return <DealsTable deals={deals} />;
    }
    
    // Good: Client Component (when needed)
    'use client';
    export function DealsTable({ deals }: { deals: Deal[] }) {
      const [filter, setFilter] = useState('');
      // Client-side interactivity
      return <div>...</div>;
    }
  ```


### Development Practices Document (`DEVELOPMENT.md`)

**Location**: Root of repository**Content**:

#### 1. Coding Standards

**Python (Backend)**:

- Follow PEP 8 style guide
- Use type hints for all functions
- Use async/await for I/O
- Maximum line length: 100 characters
- Use descriptive variable names

**TypeScript (Frontend)**:

- Use strict TypeScript mode
- Use functional components
- Use hooks for state management
- Follow React best practices
- Maximum line length: 100 characters

#### 2. Git Workflow

**Branch Naming**:

- `feature/{module}/{description}` - New features
- `fix/{module}/{description}` - Bug fixes
- `refactor/{module}/{description}` - Code refactoring
- `docs/{description}` - Documentation updates

**Commit Messages**:

```javascript
type(module): Short description

Longer description if needed

- Bullet point 1
- Bullet point 2
```

**Types**: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`**Examples**:

```javascript
feat(auth): Add MFA support for admin accounts

- Implement TOTP generation
- Add MFA verification endpoint
- Update admin login flow
```

#### 3. Testing Practices

**Unit Tests**:

- Test individual functions/components
- Mock external dependencies
- Test edge cases and error conditions
- Aim for 80%+ coverage

**Integration Tests**:

- Test module interactions
- Test API endpoints
- Test database operations
- Test authentication flows

**E2E Tests**:

- Test complete user journeys
- Use Cursor browser for visual testing
- Test error scenarios

#### 4. Code Review Process

**Review Checklist**:

- [ ] Code follows style guide
- [ ] Tests are included
- [ ] Documentation is updated
- [ ] No secrets in code
- [ ] Security considerations addressed
- [ ] Performance implications considered

**Review Process**:

1. Create PR with clear description
2. Request review from team member
3. Address review comments
4. Get approval
5. Merge to main

#### 5. Module Development Guidelines

**Before Starting**:

- Review module rules file
- Understand dependencies
- Check interface contracts
- Review similar implementations

**During Development**:

- Follow module-specific patterns
- Write tests as you code
- Document public APIs
- Keep commits atomic

**Before Completing**:

- Run all tests
- Check code coverage
- Update documentation
- Review against module rules

#### 6. Team Collaboration

**Communication**:

- Use PR comments for code discussions
- Update team on interface changes
- Document blocking issues
- Share knowledge in team meetings

**Knowledge Sharing**:

- Document complex logic
- Share learnings in team wiki
- Code review as learning opportunity
- Pair programming for complex features

### Rules File Template

**Template for `{module}/RULES.md`**:

```markdown
# {Module Name} Development Rules

## Purpose
Brief description of module purpose and responsibilities.

## Dependencies
- Depends on: [list dependencies]
- Used by: [list dependents]

## Coding Standards
- [Module-specific coding standards]

## Patterns & Best Practices
- [Module-specific patterns]

## Security Requirements
- [Security requirements for this module]

## Testing Requirements
- [Testing requirements and coverage goals]

## Examples
- [Code examples showing correct patterns]

## Common Pitfalls
- [Things to avoid]

## Resources
- [Links to relevant documentation]
```

### Rules File Maintenance

1. **Keep Rules Updated**:

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Update when patterns change
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Add new patterns as they emerge
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Remove outdated patterns

2. **Review Regularly**:

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Review rules in team meetings
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Update based on code review feedback
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Align with team decisions

3. **Enforce Rules**:

                                                                                                                                                                                                - Reference rules in code reviews
                                                                                                                                                                                                - Use linters to enforce some rules
                                                                                                                                                                                                - Document exceptions

---

## Operational Documentation & Scripts

### Overview

This section covers operational documentation files and helper scripts that ensure smooth development, deployment, and maintenance of the platform. These files standardize processes, reduce onboarding time, and ensure consistency across the team.

### Operational Documentation Files

#### 1. PREREQUISITES.md

**Purpose**: Document all machine, account, and project-level prerequisites that must be verified before development, testing, or release.

**Content**:

- **Required Developer Tools** (minimum supported versions):
  - git >= 2.34
  - node >= 18.x (use .nvmrc to pin)
  - npm or pnpm
  - python >= 3.10
  - docker >= 20.10
  - docker-compose >= 1.29
  - supabase CLI (pin version in TOOL_VERSIONS)
  - jq, curl
  - prek (pre-commit hook manager)

- **Environment Files**:
  - `.env.example` must include placeholders for:
    - DATABASE_URL
    - SUPABASE_URL
    - SUPABASE_KEY
    - SENTRY_DSN (optional)
    - FEATURE_FLAG_KEY
    - OPENAI_API_KEY / ANTHROPIC_API_KEY
    - STRIPE_SECRET_KEY
    - All other service credentials
  - Developers must copy `.env.example` -> `.env.development` and fill dev credentials

- **Accounts and Access**:
  - Ensure dev service accounts created for:
    - Supabase
    - Sentry
    - Monitoring services
    - MCP servers
  - Add dev accounts to chosen password manager (1Password / Bitwarden) with read-only secrets where appropriate

- **Local Dev Start**:
  - `./scripts/bootstrap.sh` must be run once to:
    - Create `.env.development`
    - Start local emulators
    - Seed test data
  - `./scripts/check_env.sh` validates environment on each machine

- **Test Data**:
  - Provide `tests/fixtures/` containing:
    - Small canonical CSVs
    - `scripts/generate_large_fixture.py` to simulate heavy uploads
    - Intentionally malformed CSV for error handling tests

- **Dev Container**:
  - Provide `.devcontainer/devcontainer.json` for VS Code devcontainers
  - Ensures contributors have identical environments

- **Onboarding Checklist for New Devs**:
  1. Clone repo
  2. Run `./scripts/check_env.sh`
  3. Run `./scripts/bootstrap.sh`
  4. Run `pnpm install` or `pip install -r requirements.txt`
  5. Run `pnpm test` / `pytest`
  6. Verify all checks pass

**Location**: `PREREQUISITES.md` in repository root

#### 2. SECURITY.md

**Purpose**: Document required security controls and operational runbooks.

**Content**:

- **Policy Highlights**:
  - Secrets: Never commit secrets. CI must run secret-scan that fails PRs if secrets detected
  - Dependencies: Dependabot or Renovate enabled, Snyk/OSS vulnerability scanning enabled in CI
  - Admins: MFA required for admin console access; role-based access control enforced for production systems

- **Runbook: Suspected Secret Leak**:
  1. Revoke leaked secret (immediately)
  2. Rotate the secret across environments and update CI/Secrets store
  3. Create high-priority vulnerability issue and tag security@
  4. Run full CI security-scan and audit logs to determine exposure window

- **Runtime Protections**:
  - Enforce security headers at middleware:
    - CSP (Content Security Policy)
    - HSTS (HTTP Strict Transport Security)
    - X-Frame-Options
    - X-Content-Type-Options
  - Rate limiting on public endpoints with sensible defaults and whitelisting for internal services

- **DB / RLS**:
  - Enforce Row-Level Security for user-scoped tables
  - Add automated tests that run queries with different roles to confirm deny/allow

- **CI Checks** (must be present):
  - gitleaks/detect-secrets baseline
  - SAST scanner (Bandit for Python, ESLint security rules for JS)
  - DAST quick scan on staging (OWASP ZAP nightly)

- **Vulnerability Process**:
  - CVSS score each reported issue
  - Assign SLA:
    - Critical (24h)
    - High (72h)
    - Medium (7 days)
    - Low (30 days)

- **Contact**:
  - security@<company> for incidents and triage

**Location**: `SECURITY.md` in repository root

#### 3. TESTING.md

**Purpose**: Define the testing pyramid, test ownership, and CI policies.

**Content**:

- **Test Pyramid**:
  - **Unit Tests**: Fast, local. Target 80%+ coverage for core modules. Run on every PR
  - **Integration Tests**: Run against test DB and Supabase emulator. Run on PRs and every merge to staging
  - **Contract Tests**: Validate OpenAPI/GraphQL schemas between frontend and backend in CI
  - **E2E Tests**: Playwright for critical flows (auth, upload, analyze, alerts). Run on preview/staging
  - **Visual Regression**: Snapshots for critical dashboards

- **Tools**:
  - **Unit**: pytest (Python) / Jest (Node)
  - **E2E**: Playwright
  - **Contract**: `schemathesis` or `pact` for APIs
  - **Fuzz/Property**: Hypothesis for parser modules

- **CI Integration**:
  - `ci/tests.yml` runs:
    - lint -> unit tests -> integration tests (in parallel where possible) -> publish results
  - E2E and visual regression run on staging only, triggered on merge to staging or manual PR preview

- **Test Data**:
  - `tests/fixtures/` contains canonical CSVs
  - Include one intentionally malformed CSV to assert graceful failure
  - `scripts/generate_large_fixture.py` for load testing

- **Quality Gates**:
  - PRs must not drop coverage for modified files
  - Critical modules require two reviewers and passing security checks

**Location**: `TESTING.md` in repository root

#### 4. RELEASE.md

**Purpose**: Prescribe how releases are prepared, validated, and deployed.

**Content**:

- **Branching Model**:
  - `main` -> production
  - `staging` -> pre-prod
  - Feature branches -> PRs -> reviewed -> merged to staging

- **CI Gating**:
  - Protect `main` with required status checks:
    - lint
    - unit tests
    - vulnerability scan
    - contract tests

- **Release Process**:
  1. Merge to `main` triggers `ci/release.yml` (semantic-release)
  2. CI builds artifacts, runs migration dry-run on staging, deploys to staging preview and runs smoke-tests
  3. Manual approval gate (product + dev lead) to deploy to production
  4. Post-deploy synthetic checks run for 30 minutes; if error rate exceeds threshold, rollback

- **DB Migration Policy**:
  - All migrations must be idempotent
  - Migrations run through a `ci/migration.yml` job:
    - Apply to staging DB
    - Run migration tests
    - Require manual approval for prod

- **Feature Flags**:
  - Use flags for risky features with percent rollout

- **Rollback**:
  - Document image rollback and DB compensating migration steps in `docs/rollback.md`

- **Changelogs**:
  - Enforce Conventional Commits to automatically generate changelogs and release notes

- **GitHub Projects Integration**:
  - Use GitHub Projects for release planning and tracking
  - Create release milestones in GitHub Projects
  - Track release progress in Roadmap view
  - Link issues to release milestones
  - Monitor release readiness in project board

**Location**: `RELEASE.md` in repository root

#### 5. TOOLS_AND_SUPPORT.md

**Purpose**: Standardize the toolset, versions, and support process.

**Content**:

- **Tool Versions**:
  - Add `tool-versions` file or `.nvmrc` and `python-version` files
  - Pin major tooling versions for CI reproducibility

- **Dev Container**:
  - Provide `.devcontainer/` to normalize editors and CLI tooling

- **Observability**:
  - **Error Reporting**: Sentry (DSN provided via .env)
  - **Metrics/APM**: Prometheus + Grafana or Datadog depending on budget
  - **Log Storage**: Centralized (e.g. ELK stack, Datadog logs)

- **Secrets Manager**:
  - Use 1Password or Bitwarden org vault
  - Document access request and offboarding steps

- **MCP / AI Servers**:
  - Restrict scopes
  - Store tokens in secrets manager
  - Rotate monthly
  - Provide short `docs/MCP_SERVERS.md` with:
    - Permitted endpoints
    - Auditing steps

- **Support Process**:
  - Define on-call rotation and alerting thresholds in `docs/ONCALL.md`
  - Define severity matrix and contact points for ops and product

**Location**: `TOOLS_AND_SUPPORT.md` in repository root

### Helper Scripts

#### 1. scripts/check_env.sh

**Purpose**: Validate all required developer tools are installed with version checking.

**Features**:
- Checks for: git, node, npm, python, docker, docker-compose
- Reports version information
- Exits with error if any tool missing
- Provides helpful error messages

**Usage**:
```bash
./scripts/check_env.sh
```

**Location**: `scripts/check_env.sh`

#### 2. scripts/bootstrap.sh

**Purpose**: Bootstrap development environment with one command.

**Features**:
- Copies `.env.example` to `.env.development` if not exists
- Starts local containers (supabase emulator, local db) via docker-compose
- Seeds test data if available
- Provides clear feedback on each step

**Usage**:
```bash
./scripts/bootstrap.sh
```

**Location**: `scripts/bootstrap.sh`

### CI/CD Workflows

#### 1. .github/workflows/security-scan.yml

**Purpose**: Automated security scanning on every PR.

**Features**:
- **Secret Scanning**: gitleaks to detect committed secrets
- **Dependency Scanning**: npm audit and optional Snyk scan
- **SAST**: Bandit for Python, ESLint security rules for JS
- Runs on PRs to staging and main branches
- Fails PR if critical issues found

**Location**: `.github/workflows/security-scan.yml`

#### 2. .github/workflows/tests.yml

**Purpose**: Run all tests in CI pipeline.

**Features**:
- **Lint and Unit Tests Job**:
  - Setup Node.js and Python
  - Install dependencies
  - Run linting
  - Run unit tests (parallel where possible)
- **Integration Tests Job**:
  - Start test DB via docker-compose
  - Run integration tests against test database
  - Cleanup after tests
- Runs on PRs and pushes to staging/main
- Publishes test results

**Location**: `.github/workflows/tests.yml`

#### 3. .github/workflows/release.yml

**Purpose**: Automated release management with semantic versioning.

**Features**:
- Triggered on push to main
- Uses semantic-release for:
  - Version bumping
  - Changelog generation
  - Git tag creation
  - GitHub release creation
- Respects Conventional Commits format

**Location**: `.github/workflows/release.yml`

### Additional Documentation

#### 1. docs/release_checklist.md

**Purpose**: Checklist for release validation.

**Content**:
- **Automated Checks** (must pass):
  - [ ] Lint
  - [ ] Unit tests
  - [ ] Integration tests
  - [ ] Security scans (gitleaks, vulnerability scan)
  - [ ] Contract tests (OpenAPI)
  - [ ] Migration dry-run
- **Manual Checks** (required):
  - [ ] Product signoff
  - [ ] Monitoring dashboards configured and ready
  - [ ] Runbook updated
  - [ ] On-call notified of scheduled release
- **Post-Deploy**:
  - [ ] Run synthetic checks for 30 minutes
  - [ ] Monitor error rate and latency
  - [ ] If threshold exceeded, follow rollback runbook

**Location**: `docs/release_checklist.md`

#### 2. docs/rollback.md

**Purpose**: Document rollback procedures.

**Content**:
1. Trigger quick rollback to previous stable image via deployment system
2. If DB migration applied, apply compensating migration or restore DB from snapshot
3. Notify stakeholders and open incident ticket
4. Run post-rollback verification tests

**Location**: `docs/rollback.md`

### Dev Container Setup

#### .devcontainer/devcontainer.json

**Purpose**: Normalize development environment for all contributors.

**Features**:
- Pre-configured VS Code devcontainer
- Required tools pre-installed
- Recommended extensions
- Consistent environment across team
- Faster onboarding for new developers

**Location**: `.devcontainer/devcontainer.json`

### Test Fixtures

#### tests/fixtures/

**Purpose**: Provide test data for development and testing.

**Content**:
- Canonical CSV files for standard testing
- Intentionally malformed CSV for error handling tests
- `scripts/generate_large_fixture.py` for load testing

**Location**: `tests/fixtures/`

### Implementation Checklist

- [ ] Create PREREQUISITES.md with all required tools and setup steps
- [ ] Create SECURITY.md with security policies and runbooks
- [ ] Create TESTING.md with testing strategy and quality gates
- [ ] Create RELEASE.md with release management process
- [ ] Create TOOLS_AND_SUPPORT.md with tool versions and support process
- [ ] Create scripts/check_env.sh for environment validation
- [ ] Create scripts/bootstrap.sh for environment bootstrap
- [ ] Create .github/workflows/security-scan.yml for security scanning
- [ ] Create .github/workflows/tests.yml for CI testing
- [ ] Create .github/workflows/release.yml for release automation
- [ ] Create docs/release_checklist.md for release validation
- [ ] Create docs/rollback.md for rollback procedures
- [ ] Create .devcontainer/devcontainer.json for dev container
- [ ] Create tests/fixtures/ with test data
- [ ] Create scripts/generate_large_fixture.py for load testing
- [ ] Update .env.example with all required placeholders
- [ ] Configure tool version files (.nvmrc, python-version, tool-versions)

### Benefits

1. **Standardized Onboarding**: New developers can get started quickly with clear prerequisites
2. **Security First**: Security policies and runbooks ensure consistent security practices
3. **Quality Assurance**: Testing strategy ensures code quality from the start
4. **Smooth Releases**: Release management process reduces deployment risks
5. **Consistent Environment**: Dev containers ensure all developers have identical setups
6. **Automated Checks**: CI/CD workflows catch issues early
7. **Operational Readiness**: Runbooks and checklists ensure smooth operations

---

## GitHub Projects Integration

### Overview

GitHub Projects provides a flexible project management system integrated directly with GitHub repositories. We'll use GitHub Projects to manage sprints, track tasks, monitor progress, plan releases, and organize issues. This provides a unified view of all project work within the GitHub ecosystem.

**Why GitHub Projects**:

- **Native Integration**: Seamlessly integrates with GitHub Issues, Pull Requests, and Milestones
- **Real-time Updates**: Automatic updates when issues/PRs are created, updated, or closed
- **Multiple Views**: Board view (Kanban), Table view (spreadsheet), and Roadmap view (timeline)
- **Custom Fields**: Track sprint, priority, status, assignee, and custom metadata
- **Automation**: Built-in automation rules for workflow management
- **Visibility**: All team members can see project status in real-time
- **No External Tools**: Everything managed within GitHub

### Project Structure

#### 1. Main Project Board

**Purpose**: Central project board for overall project management.

**Views**:
- **Board View**: Kanban-style board for visual task management
- **Table View**: Spreadsheet view for detailed tracking
- **Roadmap View**: Timeline view for release planning

**Fields**:
- **Status**: Todo, In Progress, In Review, Done, Blocked
- **Priority**: Critical, High, Medium, Low
- **Sprint**: Current sprint identifier (e.g., Sprint 1, Sprint 2)
- **Assignee**: Team member responsible
- **Labels**: Feature area (backend, frontend, auth, user, admin, AI, etc.)
- **Milestone**: Release milestone (v1.0, v1.1, etc.)
- **Story Points**: Effort estimation (optional)
- **Due Date**: Task deadline

**Workflows**:
- Issues automatically added to "Todo" when created
- PRs automatically linked to issues
- Status updates when PRs are merged
- Milestone tracking for releases

#### 2. Sprint Management

**Purpose**: Track work within each sprint.

**Sprint Setup**:
1. Create sprint milestone (e.g., "Sprint 1 - Foundation")
2. Assign issues to sprint milestone
3. Set sprint dates (start and end)
4. Use "Sprint" field to filter by sprint

**Sprint Board Columns**:
- **Backlog**: Issues planned for future sprints
- **Sprint Planning**: Issues being planned for current sprint
- **Todo**: Issues ready to start
- **In Progress**: Issues currently being worked on
- **In Review**: Issues in code review
- **Testing**: Issues in testing phase
- **Done**: Completed issues
- **Blocked**: Issues blocked by dependencies

**Sprint Workflow**:
1. **Sprint Planning**: Add issues to sprint milestone
2. **Daily Standup**: Review board, move cards as needed
3. **Sprint Review**: Review completed work
4. **Sprint Retrospective**: Identify improvements

**Automation Rules**:
- When issue assigned to sprint milestone → Add to "Sprint Planning"
- When PR created for issue → Move to "In Review"
- When PR merged → Move to "Done"
- When issue closed → Update status to "Done"

#### 3. Task Tracking

**Purpose**: Track individual tasks and their progress.

**Task Types**:
- **Feature**: New feature implementation
- **Bug**: Bug fix
- **Enhancement**: Feature improvement
- **Documentation**: Documentation updates
- **Refactor**: Code refactoring
- **Test**: Test implementation
- **DevOps**: Infrastructure/CI/CD work

**Task Fields**:
- **Type**: Feature, Bug, Enhancement, etc.
- **Status**: Current status in workflow
- **Priority**: Urgency level
- **Assignee**: Developer working on task
- **Labels**: Module/area (core, auth, user, admin, frontend, backend)
- **Sprint**: Current sprint
- **Story Points**: Effort estimate
- **Due Date**: Deadline
- **Dependencies**: Linked issues that must be completed first

**Task Workflow**:
1. Create issue with appropriate labels and fields
2. Issue appears in project board
3. Assign to sprint during planning
4. Move through status columns as work progresses
5. Link PRs to issues
6. Close issue when complete

#### 4. Progress Monitoring

**Purpose**: Monitor project progress and velocity.

**Metrics to Track**:
- **Sprint Velocity**: Story points completed per sprint
- **Burndown Chart**: Track remaining work over time
- **Completion Rate**: Percentage of issues completed
- **Cycle Time**: Time from start to completion
- **Blocked Issues**: Number and duration of blocked items
- **PR Review Time**: Time in review status

**Views for Monitoring**:
- **Table View**: Sort and filter by status, assignee, sprint, priority
- **Roadmap View**: See timeline of releases and milestones
- **Insights**: GitHub provides built-in insights and charts

**Progress Reports**:
- Weekly sprint progress report
- Release readiness dashboard
- Team velocity trends
- Blocked items report

#### 5. Release Planning

**Purpose**: Plan and track releases.

**Release Milestones**:
- Create milestone for each release (e.g., "v1.0.0", "v1.1.0")
- Set release date
- Assign issues to milestone
- Track milestone progress

**Release Board**:
- **Planned**: Features planned for release
- **In Development**: Features being developed
- **In Testing**: Features in QA/testing
- **Ready for Release**: Features ready to ship
- **Released**: Completed releases

**Release Workflow**:
1. Create release milestone
2. Add issues to milestone
3. Track progress in Roadmap view
4. Use release checklist (docs/release_checklist.md)
5. Tag release when complete
6. Close milestone

**Integration with CI/CD**:
- Release workflow (`.github/workflows/release.yml`) creates tags
- Tags trigger deployments
- Milestones track release progress

#### 6. Issue Management

**Purpose**: Organize and prioritize issues.

**Issue Templates**:
Create issue templates in `.github/ISSUE_TEMPLATE/`:
- **Bug Report**: Template for bug reports
- **Feature Request**: Template for feature requests
- **Question**: Template for questions
- **Documentation**: Template for documentation issues

**Issue Labels**:
- **Type**: `bug`, `feature`, `enhancement`, `documentation`, `refactor`, `test`
- **Module**: `core`, `auth`, `user`, `admin`, `frontend`, `backend`, `ai`
- **Priority**: `critical`, `high`, `medium`, `low`
- **Status**: `blocked`, `needs-review`, `in-progress`, `ready-for-qa`
- **Sprint**: `sprint-1`, `sprint-2`, etc.

**Issue Workflow**:
1. Create issue with appropriate template
2. Add labels and assign to project
3. Assign to sprint during planning
4. Link related issues (dependencies, duplicates)
5. Create PR and link to issue
6. Close issue when PR merged

**Issue Automation**:
- Auto-label based on file paths changed
- Auto-assign based on module
- Auto-close when PR merged
- Auto-move to "In Review" when PR created

### Project Views

#### 1. Board View (Kanban)

**Layout**:
```
┌─────────────┬──────────────┬─────────────┬─────────────┬──────────┐
│   Backlog   │  Todo        │ In Progress │ In Review   │   Done   │
├─────────────┼──────────────┼─────────────┼─────────────┼──────────┤
│ Issue #123  │ Issue #124   │ Issue #125  │ Issue #126  │ Issue #1 │
│ Feature     │ Bug          │ Enhancement │ Feature     │ Feature  │
│ High        │ Critical     │ Medium      │ High        │ Done     │
└─────────────┴──────────────┴─────────────┴─────────────┴──────────┘
```

**Use Cases**:
- Daily standup reviews
- Visual progress tracking
- Sprint management
- Quick status updates

#### 2. Table View (Spreadsheet)

**Columns**:
- Title
- Status
- Assignee
- Labels
- Sprint
- Priority
- Due Date
- Milestone
- Story Points

**Use Cases**:
- Detailed task tracking
- Sorting and filtering
- Bulk updates
- Progress reports

#### 3. Roadmap View (Timeline)

**Features**:
- Timeline of milestones
- Release dates
- Feature dependencies
- Sprint timeline

**Use Cases**:
- Release planning
- Long-term planning
- Dependency visualization
- Stakeholder updates

### Custom Fields

#### Status Field

**Options**:
- **Todo**: Not started
- **In Progress**: Actively being worked on
- **In Review**: Code review in progress
- **Testing**: In QA/testing
- **Done**: Completed
- **Blocked**: Blocked by dependency or issue

#### Priority Field

**Options**:
- **Critical**: Must be fixed immediately
- **High**: Important, should be done soon
- **Medium**: Normal priority
- **Low**: Nice to have, can wait

#### Sprint Field

**Format**: `Sprint {number}` or `Sprint {name}`

**Examples**:
- Sprint 1
- Sprint 2 - Foundation
- Sprint 3 - Core Features

### Automation Rules

#### 1. Auto-Status Updates

**Rules**:
- When PR created → Move issue to "In Review"
- When PR merged → Move issue to "Done"
- When issue closed → Update status to "Done"
- When issue reopened → Move to "Todo"

#### 2. Auto-Assignment

**Rules**:
- When issue labeled `backend` → Assign to backend team
- When issue labeled `frontend` → Assign to frontend team
- When issue labeled `auth` → Assign to auth module owner

#### 3. Auto-Labeling

**Rules**:
- When PR changes `backend/` → Add `backend` label
- When PR changes `frontend/` → Add `frontend` label
- When issue mentions "bug" → Add `bug` label

#### 4. Sprint Management

**Rules**:
- When issue added to milestone → Add to current sprint
- When sprint milestone closed → Archive sprint issues

### Integration with Workflows

#### 1. Issue Creation

**Workflow**:
1. Developer creates issue using template
2. Issue automatically added to project board
3. Issue appears in "Todo" column
4. Labels and fields auto-populated based on template

#### 2. Development

**Workflow**:
1. Issue assigned to developer
2. Developer moves issue to "In Progress"
3. Developer creates branch and PR
4. PR automatically links to issue
5. Issue moves to "In Review"

#### 3. Code Review

**Workflow**:
1. PR created → Issue moves to "In Review"
2. Reviewers review PR
3. Changes requested → Issue stays in "In Review"
4. PR approved → Ready to merge

#### 4. Completion

**Workflow**:
1. PR merged → Issue moves to "Done"
2. Issue automatically closed
3. Status updated in project board
4. Sprint progress updated

### Sprint Planning Process

#### 1. Pre-Sprint Planning

**Activities**:
- Review backlog
- Estimate story points
- Identify dependencies
- Set sprint goal

**Tools**:
- Table view for backlog review
- Labels for filtering
- Story points field for estimation

#### 2. Sprint Planning Meeting

**Activities**:
- Select issues for sprint
- Assign to sprint milestone
- Assign developers
- Set priorities
- Identify risks

**Tools**:
- Board view for visual planning
- Drag-and-drop to assign
- Sprint field for tracking

#### 3. Sprint Execution

**Activities**:
- Daily standups
- Update status
- Track progress
- Resolve blockers

**Tools**:
- Board view for daily updates
- Status field for tracking
- Blocked status for issues

#### 4. Sprint Review

**Activities**:
- Review completed work
- Demo features
- Gather feedback

**Tools**:
- Roadmap view for timeline
- Done column for completed items
- Milestone progress

#### 5. Sprint Retrospective

**Activities**:
- Review sprint metrics
- Identify improvements
- Update processes

**Tools**:
- Insights for metrics
- Table view for analysis
- Documentation updates

### Release Planning Process

#### 1. Release Planning

**Activities**:
- Define release scope
- Create release milestone
- Assign issues to milestone
- Set release date

**Tools**:
- Roadmap view for timeline
- Milestone tracking
- Dependency visualization

#### 2. Release Tracking

**Activities**:
- Monitor progress
- Track blockers
- Update stakeholders

**Tools**:
- Board view for status
- Table view for details
- Roadmap view for timeline

#### 3. Release Preparation

**Activities**:
- Complete release checklist
- Run tests
- Update documentation
- Prepare release notes

**Tools**:
- Release checklist (docs/release_checklist.md)
- Milestone issues
- CI/CD workflows

#### 4. Release Execution

**Activities**:
- Deploy to staging
- Run smoke tests
- Deploy to production
- Monitor post-deploy

**Tools**:
- Release workflow
- Monitoring dashboards
- Rollback procedures

### Best Practices

#### 1. Issue Management

- **Use Templates**: Always use issue templates for consistency
- **Add Labels**: Label issues appropriately for filtering
- **Link Related Issues**: Link dependencies and related issues
- **Update Status**: Keep status current as work progresses
- **Add Context**: Include screenshots, logs, and relevant information

#### 2. Sprint Management

- **Regular Updates**: Update status daily
- **Clear Goals**: Set clear sprint goals
- **Realistic Estimates**: Estimate story points realistically
- **Track Blockers**: Mark and resolve blockers quickly
- **Review Regularly**: Review progress mid-sprint

#### 3. Release Planning

- **Plan Ahead**: Plan releases 2-3 sprints ahead
- **Track Dependencies**: Identify and track dependencies early
- **Buffer Time**: Include buffer time for unexpected issues
- **Stakeholder Updates**: Regular updates to stakeholders
- **Documentation**: Keep release notes updated

#### 4. Automation

- **Use Automation**: Leverage automation rules for efficiency
- **Review Rules**: Regularly review and update automation rules
- **Test Rules**: Test automation rules before deploying
- **Monitor Results**: Monitor automation results

### Setup Checklist

- [ ] Create main project board
- [ ] Configure board views (Board, Table, Roadmap)
- [ ] Set up custom fields (Status, Priority, Sprint, Assignee, Labels)
- [ ] Create issue templates (Bug, Feature, Question, Documentation)
- [ ] Define issue labels (Type, Module, Priority, Status, Sprint)
- [ ] Set up automation rules (status updates, assignments, labeling)
- [ ] Create first sprint milestone
- [ ] Create release milestones (v1.0, v1.1, etc.)
- [ ] Configure project views and filters
- [ ] Document project workflow in README
- [ ] Train team on GitHub Projects usage
- [ ] Set up project insights and reporting

### Integration with Existing Workflows

#### CI/CD Integration

- PRs automatically linked to issues
- Status updates when PRs are merged
- Release workflow creates tags from milestones
- Deployment status tracked in project

#### Documentation Integration

- Release checklist (docs/release_checklist.md) references milestones
- Sprint planning documented in project
- Progress tracked in project board

#### Team Collaboration

- All team members have access to project
- Real-time updates visible to all
- Comments and discussions on issues
- Notifications for status changes

### Benefits

1. **Unified View**: All project work in one place
2. **Real-time Updates**: Automatic updates from GitHub
3. **Flexible Views**: Board, Table, and Roadmap views
4. **Automation**: Built-in automation reduces manual work
5. **Integration**: Seamless integration with Issues, PRs, and Milestones
6. **Visibility**: All team members see project status
7. **Tracking**: Comprehensive progress tracking and metrics
8. **Planning**: Effective sprint and release planning

---

## GitHub Projects Automation

### Overview

GitHub Projects can be fully automated using GitHub Actions, GitHub API, and intelligent branch/PR naming conventions. This enables zero-touch project management where issues are auto-created, status is auto-updated, and progress is tracked automatically as development progresses.

**Benefits of Full Automation**:

- **Zero Manual Work**: Issues created automatically from branch names
- **Real-time Updates**: Project board updates instantly on PR events
- **No Context Loss**: All work automatically tracked
- **Progress Visibility**: Always know project status
- **Sprint Tracking**: Automatic sprint progress updates
- **Release Planning**: Automatic milestone tracking

### Automation Strategy

#### 1. Auto-Create Issues from Branch Names

**Branch Naming Convention**:

```
{type}/{module}-{description}
```

**Examples**:
- `feature/auth-login` → Creates issue: "Implement login feature"
- `bug/user-deals-filter` → Creates issue: "Fix deals filter bug"
- `enhancement/admin-dashboard` → Creates issue: "Enhance admin dashboard"
- `refactor/core-parser` → Creates issue: "Refactor parser module"

**GitHub Action**: `.github/workflows/auto-issue-from-branch.yml`

**Features**:
- Detects new branch creation
- Parses branch name to extract type, module, description
- Creates GitHub issue with appropriate template
- Adds issue to GitHub Project
- Sets labels based on type and module
- Assigns to appropriate developer (optional)

#### 2. Auto-Update Project Status from PR Events

**PR Events**:
- **PR Opened** → Move issue to "In Review"
- **PR Ready for Review** → Move to "In Review"
- **PR Approved** → Keep in "In Review" (waiting for merge)
- **PR Merged** → Move to "Done", close issue
- **PR Closed (not merged)** → Move back to "Todo" or "In Progress"

**GitHub Action**: `.github/workflows/auto-update-project.yml`

**Features**:
- Listens to PR events (opened, ready_for_review, closed, merged)
- Finds linked issue (from PR description or branch name)
- Updates project card status
- Updates issue status
- Adds comments to issue

#### 3. Auto-Link PRs to Issues

**Methods**:
1. **Branch Name Matching**: PR branch name matches issue title
2. **PR Description**: Issue number in PR description (`Closes #123`)
3. **Commit Messages**: Issue number in commit (`fixes #123`)

**GitHub Action**: `.github/workflows/auto-link-pr.yml`

**Features**:
- Auto-detects issue from PR branch name
- Auto-links PR to issue
- Updates issue with PR link
- Moves issue to appropriate status

#### 4. Auto-Assign Based on Patterns

**Assignment Rules**:
- Branch contains `backend/` → Assign to backend team
- Branch contains `frontend/` → Assign to frontend team
- Branch contains `auth/` → Assign to auth module owner
- Issue labeled `bug` → Assign to bug triage team
- Issue labeled `critical` → Assign to on-call

**GitHub Action**: `.github/workflows/auto-assign.yml`

#### 5. Auto-Create Sprint Milestones

**Trigger**: When sprint planning document updated or sprint starts

**Features**:
- Creates milestone for new sprint
- Sets sprint dates
- Links issues to milestone
- Updates project board

#### 6. Auto-Update Sprint Progress

**Features**:
- Tracks completed issues per sprint
- Updates sprint velocity
- Generates sprint reports
- Updates sprint burndown

### Implementation

#### Branch Naming Convention

**Format**: `{type}/{module}-{kebab-case-description}`

**Types**:
- `feature/` - New features
- `bug/` - Bug fixes
- `enhancement/` - Feature improvements
- `refactor/` - Code refactoring
- `docs/` - Documentation
- `test/` - Tests
- `chore/` - Maintenance tasks

**Modules**:
- `auth` - Authentication
- `user` - User features
- `admin` - Admin features
- `core` - Core functionality
- `frontend` - Frontend work
- `backend` - Backend work
- `ai` - AI features

**Examples**:
```
feature/auth-login-implementation
bug/user-deals-sorting-issue
enhancement/admin-dashboard-stats
refactor/core-csv-parser
docs/api-authentication-guide
test/user-watchlist-integration
chore/update-dependencies
```

#### GitHub Actions Workflows

##### 1. Auto-Create Issue from Branch

**File**: `.github/workflows/auto-issue-from-branch.yml`

```yaml
name: Auto Create Issue from Branch

on:
  create:
    branches:
      - '**'

jobs:
  create-issue:
    runs-on: ubuntu-latest
    if: github.event.ref_type == 'branch'
    steps:
      - name: Parse branch name
        id: parse-branch
        run: |
          BRANCH_NAME="${{ github.event.ref }}"
          TYPE=$(echo $BRANCH_NAME | cut -d'/' -f1)
          REST=$(echo $BRANCH_NAME | cut -d'/' -f2-)
          MODULE=$(echo $REST | cut -d'-' -f1)
          DESCRIPTION=$(echo $REST | cut -d'-' -f2- | sed 's/-/ /g')
          
          echo "type=$TYPE" >> $GITHUB_OUTPUT
          echo "module=$MODULE" >> $GITHUB_OUTPUT
          echo "description=$DESCRIPTION" >> $GITHUB_OUTPUT
          echo "branch=$BRANCH_NAME" >> $GITHUB_OUTPUT

      - name: Create issue
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const { type, module, description, branch } = process.env;
            
            const title = `${type}: ${description}`;
            const body = `
            ## Branch
            \`${branch}\`
            
            ## Type
            ${type}
            
            ## Module
            ${module}
            
            ## Description
            ${description}
            
            ## Auto-generated
            This issue was automatically created from branch \`${branch}\`
            `;
            
            const labels = [type, module];
            const issue = await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: title,
              body: body,
              labels: labels
            });
            
            // Add to project
            // (Project API calls here)
            
            console.log(`Created issue #${issue.data.number}`);
```

##### 2. Auto-Update Project on PR Events

**File**: `.github/workflows/auto-update-project.yml`

```yaml
name: Auto Update Project on PR

on:
  pull_request:
    types: [opened, ready_for_review, closed, merged]

jobs:
  update-project:
    runs-on: ubuntu-latest
    steps:
      - name: Find linked issue
        id: find-issue
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const pr = context.payload.pull_request;
            const branch = pr.head.ref;
            
            // Parse branch to find issue
            // Or check PR description for issue number
            // Or check commit messages
            
            // Find issue number
            const issueNumber = extractIssueNumber(branch, pr.body);
            
            return issueNumber;

      - name: Update project status
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const event = context.payload.action;
            const issueNumber = '${{ steps.find-issue.outputs.issue-number }}';
            
            let newStatus = '';
            if (event === 'opened' || event === 'ready_for_review') {
              newStatus = 'In Review';
            } else if (event === 'merged') {
              newStatus = 'Done';
            } else if (event === 'closed') {
              newStatus = 'Todo'; // PR closed without merge
            }
            
            // Update project card status
            // Update issue status
```

##### 3. Auto-Link PR to Issue

**File**: `.github/workflows/auto-link-pr.yml`

```yaml
name: Auto Link PR to Issue

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  link-issue:
    runs-on: ubuntu-latest
    steps:
      - name: Extract issue from branch
        id: extract-issue
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const branch = context.payload.pull_request.head.ref;
            // Parse branch name to find matching issue
            // Or search issues by title matching branch description
            
            const issueNumber = findMatchingIssue(branch);
            return issueNumber;

      - name: Link PR to issue
        if: steps.extract-issue.outputs.issue-number != ''
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const issueNumber = '${{ steps.extract-issue.outputs.issue-number }}';
            const prNumber = context.payload.pull_request.number;
            
            // Add PR link to issue
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: issueNumber,
              body: `🔗 Linked PR: #${prNumber}`
            });
            
            // Update PR description with issue link
            await github.rest.pulls.update({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: prNumber,
              body: `Closes #${issueNumber}\n\n${context.payload.pull_request.body}`
            });
```

##### 4. Auto-Assign Based on Patterns

**File**: `.github/workflows/auto-assign.yml`

```yaml
name: Auto Assign

on:
  issues:
    types: [opened]
  pull_request:
    types: [opened]

jobs:
  assign:
    runs-on: ubuntu-latest
    steps:
      - name: Auto assign
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const labels = context.payload.issue?.labels || context.payload.pull_request.labels || [];
            const title = context.payload.issue?.title || context.payload.pull_request.title || '';
            const body = context.payload.issue?.body || context.payload.pull_request.body || '';
            
            let assignee = null;
            
            // Assign based on labels
            if (labels.some(l => l.name === 'backend')) {
              assignee = 'backend-team-member';
            } else if (labels.some(l => l.name === 'frontend')) {
              assignee = 'frontend-team-member';
            } else if (labels.some(l => l.name === 'auth')) {
              assignee = 'auth-module-owner';
            }
            
            // Assign based on title/body keywords
            if (title.includes('critical') || body.includes('critical')) {
              assignee = 'on-call-engineer';
            }
            
            if (assignee) {
              await github.rest.issues.addAssignees({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: context.issue?.number || context.payload.pull_request.number,
                assignees: [assignee]
              });
            }
```

#### PR Templates

**File**: `.github/pull_request_template.md`

```markdown
## Description
<!-- Auto-filled from branch name if possible -->

## Related Issue
<!-- Auto-linked from branch name -->
Closes #

## Type of Change
- [ ] Feature
- [ ] Bug fix
- [ ] Enhancement
- [ ] Refactor
- [ ] Documentation
- [ ] Test

## Module
- [ ] Auth
- [ ] User
- [ ] Admin
- [ ] Core
- [ ] Frontend
- [ ] Backend
- [ ] AI

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] E2E tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
```

#### Issue Templates

**File**: `.github/ISSUE_TEMPLATE/feature.yml`

```yaml
name: Feature Request
description: Request a new feature
title: "[Feature] "
labels: ["feature"]
body:
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Describe the feature
      placeholder: What should this feature do?
  - type: dropdown
    id: module
    attributes:
      label: Module
      options:
        - Auth
        - User
        - Admin
        - Core
        - Frontend
        - Backend
        - AI
  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - Critical
        - High
        - Medium
        - Low
```

### GitHub Projects API Integration

#### Using GitHub Projects API

**Authentication**: Use `GITHUB_TOKEN` or Personal Access Token with `project` scope

**Key Operations**:
1. **Add Issue to Project**: Add issue to project board
2. **Update Card Status**: Move card between columns
3. **Update Custom Fields**: Update sprint, priority, etc.
4. **Link PR to Issue**: Connect PR to project card

**Example Script**:

```typescript
// .github/scripts/update-project.ts
import { Octokit } from '@octokit/rest';

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

async function addIssueToProject(issueNumber: number, projectId: string) {
  // Get project
  const project = await octokit.projects.get({
    project_id: parseInt(projectId)
  });
  
  // Add issue to project
  await octokit.projects.createCard({
    column_id: columnId, // "Todo" column
    content_id: issueNumber,
    content_type: 'Issue'
  });
}

async function updateCardStatus(cardId: string, newStatus: string) {
  // Find column ID for new status
  const columnId = getColumnIdForStatus(newStatus);
  
  // Move card
  await octokit.projects.moveCard({
    card_id: parseInt(cardId),
    position: 'top',
    column_id: columnId
  });
}
```

### Automation Rules Summary

#### Branch → Issue

- **Trigger**: New branch created
- **Action**: Create issue from branch name
- **Add to**: Project board "Todo" column
- **Labels**: Auto-assign based on branch type and module

#### PR Opened → Status Update

- **Trigger**: PR opened or ready for review
- **Action**: Find linked issue, move to "In Review"
- **Update**: Issue status, project card status

#### PR Merged → Complete

- **Trigger**: PR merged
- **Action**: Move issue to "Done", close issue
- **Update**: Sprint progress, milestone progress

#### PR Closed → Reopen

- **Trigger**: PR closed without merge
- **Action**: Move issue back to "Todo" or "In Progress"

#### Commit Message → Link

- **Trigger**: Commit with issue number
- **Action**: Auto-link commit to issue
- **Update**: Issue activity

### Complete Automation Workflow

```
Developer creates branch: feature/auth-login
    ↓
GitHub Action: Auto-create issue #123 "Feature: auth login"
    ↓
Issue added to Project "Todo" column
    ↓
Developer opens PR: feature/auth-login → main
    ↓
GitHub Action: Auto-link PR #45 to issue #123
    ↓
GitHub Action: Move issue #123 to "In Review"
    ↓
PR reviewed and approved
    ↓
PR merged
    ↓
GitHub Action: Move issue #123 to "Done"
    ↓
GitHub Action: Close issue #123
    ↓
Sprint progress updated automatically
```

### Setup Checklist

- [ ] Create branch naming convention document
- [ ] Setup `.github/workflows/auto-issue-from-branch.yml`
- [ ] Setup `.github/workflows/auto-update-project.yml`
- [ ] Setup `.github/workflows/auto-link-pr.yml`
- [ ] Setup `.github/workflows/auto-assign.yml`
- [ ] Create PR template (`.github/pull_request_template.md`)
- [ ] Create issue templates (`.github/ISSUE_TEMPLATE/`)
- [ ] Configure GitHub Projects API access
- [ ] Test automation with sample branch/PR
- [ ] Document automation rules for team
- [ ] Setup project webhooks (if needed)

### Benefits

1. **Zero Manual Work**: Everything automated
2. **Always Up-to-Date**: Project board reflects current state
3. **No Context Loss**: All work automatically tracked
4. **Progress Visibility**: Real-time progress updates
5. **Sprint Tracking**: Automatic sprint progress
6. **Release Planning**: Automatic milestone tracking
7. **Team Efficiency**: Developers focus on code, not project management

### Limitations & Considerations

1. **Branch Naming**: Requires consistent branch naming
2. **Issue Matching**: May need fuzzy matching for branch→issue
3. **API Rate Limits**: GitHub API has rate limits
4. **Token Permissions**: Requires appropriate GitHub token permissions
5. **Error Handling**: Need robust error handling for edge cases

---

## Sprint Planning & Structure

### Overview

This section defines the sprint-wise breakdown of the project, starting with Sprint 0 (foundation) and subsequent sprints for feature development. Each sprint is designed to be trackable in GitHub Projects with clear deliverables and success criteria.

### Sprint 0: Foundation & Decisions (Solo-Dev Optimized)

**Duration**: 1-2 days  
**Goal**: Lock decisions, setup foundation, avoid future rework  
**Mindset**: Speed, Safety, Sanity - not scale or compliance

#### Sprint 0 Objectives

1. **Lock Decisions Once** - Avoid rework later
2. **Optimize for Future You** - Prevent context loss
3. **Security Minimum Viable** - Avoid footguns, not enterprise-grade
4. **Testing Essentials Only** - Protect, don't over-engineer
5. **CI That Protects** - Answer "Can I safely deploy?"
6. **Release Discipline** - Simple, solo-friendly process

#### Sprint 0 Tasks

##### 1. Lock Decisions (docs/decisions.md)

**Must Do** (30 minutes):

- [ ] Create `docs/decisions.md` with final decisions:
  - **Backend**: FastAPI (Python 3.11+) - FINAL
  - **Frontend**: Next.js 14+ App Router (TypeScript) - FINAL
  - **Database**: Supabase (PostgreSQL) - FINAL
  - **Hosting**: Vercel (frontend), Railway/Render (backend) - FINAL
  - **Auth Strategy**: Supabase Auth with JWT - FINAL
  - **CSV Ingestion**: Batch processing (not streaming for v1) - FINAL
  - **What NOT in v1**: Mobile apps, real-time notifications, multiple exchanges, public API, white-label - FINAL

**Rule**: Once written, don't revisit unless there's a blocker.

**Todo**: `decision-documentation`

##### 2. Repository & Basic Setup

**Must Do** (2-3 hours):

- [ ] Initialize both repositories:
  - `nse-bulk-deals-analyzer` (Application)
  - `nse-bulk-deals-analyzer-marketing` (Marketing)
- [ ] Setup branch protection on `main` branch
- [ ] Create `.gitignore` for Python, Node.js, and environment files
- [ ] Create initial `README.md` with:
  - What this app does (1 paragraph)
  - How to run locally (3 commands max)
  - How to deploy (basic steps)
- [ ] Create `PREREQUISITES.md` (from our plan)
- [ ] Create `scripts/bootstrap.sh` (from our plan)
- [ ] Create `scripts/check_env.sh` (from our plan)

**Todos**: `setup-git-worktree`, `documentation-prerequisites`, `scripts-check-env`, `scripts-bootstrap`

##### 3. Secret Management & Security Basics

**Must Do** (1-2 hours):

- [ ] Create `.env.example` with ALL placeholders:
  - DATABASE_URL
  - SUPABASE_URL, SUPABASE_KEY
  - SENTRY_DSN (optional)
  - OPENAI_API_KEY / ANTHROPIC_API_KEY
  - STRIPE_SECRET_KEY
  - All other service credentials
- [ ] Verify `.gitignore` excludes `.env*` files
- [ ] Setup secret scanning in CI (gitleaks) - `.github/workflows/security-scan.yml`
- [ ] Document: Never commit real secrets

**Todos**: `setup-secrets-management`, `setup-cicd-secrets`, `cicd-security-scan`

##### 4. CSV Fixture & Parser Skeleton

**Must Do** (1-2 hours):

- [ ] Commit at least one canonical CSV fixture to `tests/fixtures/`
  - Use real NSE bulk deals format (even with fake data)
  - Include intentionally malformed CSV for error handling
- [ ] Create parser skeleton:
  - `backend/app/core/parser.py` (basic structure)
  - `backend/app/core/models.py` (Pydantic models for bulk deals)
- [ ] One unit test for CSV parsing (minimal, but working)

**Todos**: `test-fixtures-setup`, `parser-models` (skeleton only)

##### 5. Database Schema Draft

**Must Do** (2-3 hours):

- [ ] Setup Supabase project
- [ ] Draft core database schema (even if incomplete):
  - `user_profiles` table (basic structure)
  - `bulk_deals` table (basic structure)
  - Enable Row-Level Security (RLS) ON from day one
- [ ] Create first migration file (even if minimal)
- [ ] Document backup strategy (even if manual for now)

**Todos**: `setup-supabase`, `database-schema` (draft)

##### 6. Basic CI Setup

**Must Do** (1-2 hours):

- [ ] Create `.github/workflows/tests.yml` with:
  - Lint (ruff for Python, ESLint for TypeScript)
  - Unit tests (pytest, Jest)
  - Secret scan (gitleaks)
  - Build check
- [ ] E2E tests only on `main`, not every commit
- [ ] CI answers: "Can I safely deploy this?"

**Todos**: `cicd-tests`, `setup-pre-commit-hooks`

##### 7. Release Discipline

**Must Do** (30 minutes):

- [ ] Create `RELEASE.md` with:
  - `main` = always deployable
  - Tag releases manually (v0.1.0, v0.2.0)
  - One-click rollback (previous build)
  - Simple process, no complex pipelines
- [ ] Create `.github/workflows/release.yml` (basic, semantic-release optional for now)

**Todos**: `documentation-release-management`, `cicd-release`

##### 8. Testing Essentials

**Must Do** (2-3 hours):

- [ ] Unit tests for:
  - CSV parsing (1-2 tests)
  - Business rules (filtering BUY deals, sorting) - 1-2 tests
  - Auth/permissions (basic) - 1-2 tests
- [ ] One integration test:
  - Upload CSV → process → store result
- [ ] One E2E happy path (Playwright):
  - User can login → view deals → basic flow
- [ ] **Total: 10-15 tests maximum** - that's fine for Sprint 0

**Todos**: Setup testing infrastructure (minimal), create first tests

##### 9. GitHub Projects Setup

**Must Do** (30 minutes):

- [ ] Create GitHub Project board
- [ ] Setup Sprint 0 milestone
- [ ] Create issues for each Sprint 0 task
- [ ] Configure basic fields (Status, Priority)
- [ ] Link issues to Sprint 0 milestone

**Optional** (can do in Sprint 1):

- [ ] Setup GitHub Projects automation workflows
- [ ] Configure branch naming conventions
- [ ] Setup PR and issue templates
- [ ] Test automation with sample branch/PR

**Todos**: `setup-github-projects` (required), `github-projects-automation` (optional for Sprint 0)

#### Sprint 0 Checklist (Solo Version)

**Must Do** (1-2 days max):

- [ ] Repo initialized + branch protection on main
- [ ] `.env.example` ready with all placeholders
- [ ] `bootstrap.sh` works
- [ ] Secret scan in CI
- [ ] One CSV fixture committed
- [ ] Basic README written
- [ ] DB schema drafted (even if incomplete)
- [ ] `docs/decisions.md` created and locked
- [ ] Basic CI working (lint, tests, secret scan)
- [ ] 10-15 essential tests written
- [ ] `RELEASE.md` written
- [ ] GitHub Projects setup

**Nice to Have** (can do later):

- [ ] Dev container (`.devcontainer/devcontainer.json`)
- [ ] Feature flags
- [ ] Advanced observability
- [ ] MCP servers (can wait)
- [ ] Git worktree (can wait if solo)

#### Sprint 0 Deliverables

1. **Documentation**:
   - `docs/decisions.md` - Locked decisions
   - `README.md` - Basic project overview
   - `PREREQUISITES.md` - Developer setup
   - `RELEASE.md` - Release process
   - `.env.example` - All environment variables

2. **Scripts**:
   - `scripts/check_env.sh` - Environment validation
   - `scripts/bootstrap.sh` - Bootstrap script

3. **Infrastructure**:
   - Repositories initialized
   - Branch protection configured
   - Supabase project created
   - Basic database schema (draft)
   - CI/CD workflows (basic)

4. **Code**:
   - Parser skeleton
   - CSV fixture
   - 10-15 essential tests
   - Basic project structure

5. **Security**:
   - Secret scanning in CI
   - `.gitignore` configured
   - RLS enabled on database

#### Sprint 0 Success Criteria

- [ ] Can run `./scripts/bootstrap.sh` successfully
- [ ] Can run `./scripts/check_env.sh` without errors
- [ ] CI passes (lint, tests, secret scan)
- [ ] Can parse one CSV fixture
- [ ] Database connection works
- [ ] One E2E test passes
- [ ] All decisions documented and locked
- [ ] GitHub Projects configured

**After Sprint 0**: Start building features immediately.

### Sprint Structure (Post Sprint 0)

#### Sprint 1: Core Infrastructure (Week 1)

**Goal**: Complete foundation setup and basic backend/frontend structure

**Tasks**:
- Complete database schema (all tables)
- Backend core module (complete)
- Frontend core setup (Next.js, TypeScript, Tailwind)
- Basic authentication (Supabase Auth integration)
- Module structure (backend and frontend)

**Deliverables**:
- Working database with RLS
- Backend API structure
- Frontend app structure
- Basic auth flow

**GitHub Milestone**: `Sprint 1 - Core Infrastructure`

#### Sprint 2: Authentication & User Management (Week 2)

**Goal**: Complete authentication and user profile management

**Tasks**:
- Login/Signup endpoints
- Password reset
- User profile management
- Frontend auth pages (login, signup, profile)
- Auth context and protected routes

**Deliverables**:
- Working authentication
- User can sign up and login
- Profile management working

**GitHub Milestone**: `Sprint 2 - Authentication`

#### Sprint 3: NSE Data Fetching & Parsing (Week 3)

**Goal**: Fetch and parse NSE bulk deals data

**Tasks**:
- NSE data fetcher (complete)
- CSV parser (complete)
- Data models (complete)
- Database storage
- Basic error handling

**Deliverables**:
- Can fetch NSE data
- Can parse CSV
- Data stored in database

**GitHub Milestone**: `Sprint 3 - Data Fetching`

#### Sprint 4: Deals Display & Filtering (Week 4)

**Goal**: Users can view and filter bulk deals

**Tasks**:
- Deals API endpoints
- Frontend deals page
- Filtering (BUY/SELL, date range, symbol)
- Sorting (quantity, price, date)
- Data table component

**Deliverables**:
- Users can view deals
- Filtering and sorting working

**GitHub Milestone**: `Sprint 4 - Deals Display`

#### Sprint 5: Analytics & Charts (Week 5)

**Goal**: Basic analytics and data visualization

**Tasks**:
- Analytics API endpoints
- Chart components (Recharts)
- Analytics page
- Basic visualizations (line, bar charts)

**Deliverables**:
- Analytics page working
- Charts displaying data

**GitHub Milestone**: `Sprint 5 - Analytics`

#### Sprint 6: Watchlists & Alerts (Week 6)

**Goal**: Users can create watchlists and alerts

**Tasks**:
- Watchlist API endpoints
- Alert API endpoints
- Frontend watchlist page
- Frontend alerts page
- Basic alert logic

**Deliverables**:
- Watchlists working
- Alerts working

**GitHub Milestone**: `Sprint 6 - Watchlists & Alerts`

#### Sprint 7: Admin Module (Week 7)

**Goal**: Admin can manage system and users

**Tasks**:
- Admin dashboard
- User management
- Data management
- System settings

**Deliverables**:
- Admin panel working
- Admin can manage users and data

**GitHub Milestone**: `Sprint 7 - Admin Module`

#### Sprint 8: AI Analyzer (Week 8)

**Goal**: AI-powered natural language querying

**Tasks**:
- AI SDK setup
- RAG implementation
- AI service endpoints
- Frontend AI chat interface
- Tool calling for data queries

**Deliverables**:
- AI analyzer working
- Users can ask questions about data

**GitHub Milestone**: `Sprint 8 - AI Analyzer`

#### Sprint 9: Monetization (Week 9)

**Goal**: Subscription and referral system

**Tasks**:
- Subscription plans
- Stripe integration
- Referral system
- Feature gating
- Billing pages

**Deliverables**:
- Subscriptions working
- Referral system working

**GitHub Milestone**: `Sprint 9 - Monetization`

#### Sprint 10: Security & Polish (Week 10)

**Goal**: Security hardening and polish

**Tasks**:
- Complete security implementation
- Performance optimization
- Testing (expand test coverage)
- Documentation
- Bug fixes

**Deliverables**:
- Security measures in place
- Performance optimized
- Documentation complete

**GitHub Milestone**: `Sprint 10 - Security & Polish`

#### Sprint 11: Marketing Website (Week 11)

**Goal**: Launch marketing website

**Tasks**:
- Marketing website setup
- Landing page
- Blog system
- Case studies
- Resources
- Help center

**Deliverables**:
- Marketing website live

**GitHub Milestone**: `Sprint 11 - Marketing Website`

#### Sprint 12: Launch Preparation (Week 12)

**Goal**: Prepare for production launch

**Tasks**:
- Staging validation
- Load testing
- Security audit
- Final bug fixes
- Launch checklist

**Deliverables**:
- Ready for production launch

**GitHub Milestone**: `Sprint 12 - Launch Prep`

### Sprint Planning Process

#### 1. Pre-Sprint Planning

**Activities**:
- Review previous sprint
- Identify backlog items
- Estimate effort
- Set sprint goal
- Create sprint milestone in GitHub

**Tools**:
- GitHub Projects (Table view for backlog)
- GitHub Milestones
- Issue labels

#### 2. Sprint Planning Meeting

**Activities**:
- Select issues for sprint
- Assign to developers
- Set priorities
- Create sprint board
- Define success criteria

**Tools**:
- GitHub Projects (Board view)
- GitHub Milestones
- Issue assignment

#### 3. Sprint Execution

**Activities**:
- Daily updates (status changes)
- Track progress
- Resolve blockers
- Code reviews
- Testing

**Tools**:
- GitHub Projects (Board view)
- GitHub Issues
- Pull Requests

#### 4. Sprint Review

**Activities**:
- Demo completed work
- Review metrics
- Gather feedback

**Tools**:
- GitHub Projects (Roadmap view)
- GitHub Milestones
- Completed issues

#### 5. Sprint Retrospective

**Activities**:
- Review sprint metrics
- Identify improvements
- Update processes

**Tools**:
- GitHub Projects (Insights)
- Sprint metrics

### GitHub Projects Sprint Configuration

#### Sprint Board Columns

```
┌──────────┬──────────────┬─────────────┬─────────────┬──────────┐
│ Backlog  │ Sprint Plan  │ Todo        │ In Progress │ Done     │
└──────────┴──────────────┴─────────────┴─────────────┴──────────┘
```

#### Sprint Fields

- **Sprint**: Current sprint number (Sprint 0, Sprint 1, etc.)
- **Status**: Backlog, Todo, In Progress, In Review, Done
- **Priority**: Critical, High, Medium, Low
- **Assignee**: Developer working on task
- **Story Points**: Effort estimate (optional)
- **Milestone**: Sprint milestone

#### Sprint Automation

- When issue added to sprint milestone → Add to sprint board
- When PR created → Move to "In Review"
- When PR merged → Move to "Done"
- When sprint milestone closed → Archive sprint issues

### Sprint Metrics

#### Track Per Sprint

- **Velocity**: Story points completed
- **Burndown**: Remaining work over time
- **Completion Rate**: Percentage of issues completed
- **Cycle Time**: Average time from start to completion
- **Blocked Issues**: Number and duration

#### Sprint Reports

- **Sprint Review**: Completed work summary
- **Sprint Retrospective**: What went well, what to improve
- **Velocity Trend**: Track velocity over time

### Best Practices

1. **Sprint 0 First**: Complete Sprint 0 before any feature work
2. **Lock Decisions**: Document decisions in Sprint 0, don't revisit
3. **Minimal Viable**: Focus on essentials, not perfection
4. **Track in GitHub**: Use GitHub Projects for all sprint tracking
5. **Regular Updates**: Update status daily
6. **Clear Goals**: Each sprint has a clear, achievable goal
7. **Realistic Estimates**: Don't over-commit
8. **Review Regularly**: Sprint review and retrospective

---