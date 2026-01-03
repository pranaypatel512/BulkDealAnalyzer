# Technical Decisions

**Status**: LOCKED - Do not revisit unless there's a blocker  
**Last Updated**: Sprint 0  
**Rule**: Once written, don't revisit unless there's a blocker

## Backend Language & Runtime

**Decision**: FastAPI (Python 3.11+)

**Rationale**:
- Fast, modern Python web framework
- Built-in API documentation (OpenAPI/Swagger)
- Type hints support
- Async/await support
- Large ecosystem

**Version**: Python 3.11+ (LTS)

**Status**: ✅ FINAL

---

## Frontend Stack

**Decision**: Next.js 14+ App Router (TypeScript)

**Rationale**:
- Server Components for performance
- Built-in routing and API routes
- TypeScript for type safety
- Excellent developer experience
- Great for SEO and performance

**Version**: Next.js 14+ (App Router)

**Status**: ✅ FINAL

---

## Database & Hosting

**Decision**: Supabase (PostgreSQL)

**Rationale**:
- Managed PostgreSQL database
- Built-in authentication
- Row Level Security (RLS)
- Real-time capabilities
- Generous free tier
- Easy scaling

**Status**: ✅ FINAL

---

## Hosting Strategy

**Decision**:
- **Frontend**: Vercel
- **Backend**: Railway/Render/Fly.io

**Rationale**:
- Vercel optimized for Next.js
- Easy deployments and previews
- Global CDN
- Backend platforms support FastAPI well
- Good free tiers for development

**Status**: ✅ FINAL

---

## Authentication Strategy

**Decision**: Supabase Auth with JWT tokens

**Rationale**:
- Integrated with Supabase database
- Built-in user management
- JWT token-based authentication
- Email/password authentication
- Easy to extend with OAuth later

**Status**: ✅ FINAL

---

## CSV Ingestion Approach

**Decision**: Batch processing (not streaming for v1)

**Rationale**:
- Simpler implementation
- NSE bulk deals are daily files (not real-time)
- Batch processing sufficient for v1
- Can optimize to streaming later if needed

**Status**: ✅ FINAL

---

## What NOT in v1.0

**Explicitly Out of Scope**:

1. **Mobile Native Apps**: iOS and Android apps
   - Web app is responsive, native apps can come later

2. **Real-time Notifications**: Push notifications, email alerts
   - In-app notifications only for v1.0

3. **Multiple Stock Exchanges**: Only NSE for v1.0
   - BSE and other exchanges can be added later

4. **Public API for Third Parties**: No external API access
   - Internal API only, public API can be v2.0 feature

5. **White-label Solution**: Custom branding for enterprise
   - Standard branding for v1.0

6. **Advanced Analytics**: Sector-wise analysis, correlation analysis
   - Basic analytics only for v1.0

7. **Data Export**: PDF reports, Excel exports
   - Can be added in future releases

8. **Social Features**: Sharing, comments, community features
   - Not in scope for v1.0

**Status**: ✅ FINAL

---

## Architecture Decisions

**Decision**: Multi-module architecture

**Backend Modules**:
- `core` - Foundation (database, security, utilities)
- `auth` - Authentication and authorization
- `user` - User features (deals, analytics, watchlists)
- `admin` - Admin features
- `shared` - Shared utilities

**Frontend Modules**:
- `lib/core` - Core utilities and services
- `modules/auth` - Authentication module
- `modules/user` - User features module
- `modules/admin` - Admin module
- `components` - Shared components
- `design-system` - Design system

**Status**: ✅ FINAL

---

## Repository Structure

**Decision**: Two separate repositories

1. **Application Repository**: `bulkdeal-analyzer`
   - Main product application
   - Backend and frontend code

2. **Marketing Repository**: `bulkdeal-analyzer-marketing`
   - Marketing website
   - Landing page, blog, case studies

**Status**: ✅ FINAL

---

## Development Tools

**Decision**:
- **Pre-commit Hooks**: prek (Rust-based, faster than pre-commit)
- **Linting**: ruff (Python), ESLint (TypeScript)
- **Formatting**: ruff format (Python), Prettier (TypeScript)
- **Testing**: pytest (Python), Jest + Playwright (Frontend)

**Status**: ✅ FINAL

---

## AI Integration

**Decision**: Vercel AI SDK

**Rationale**:
- Unified API for multiple providers
- Built-in streaming support
- RAG support via Language Model Middleware
- Tool calling support
- UI hooks for chat interfaces

**Status**: ✅ FINAL

---

## Payment Processing

**Decision**: Stripe

**Rationale**:
- Industry standard
- Good documentation
- Easy integration
- Supports subscriptions
- Available in target markets

**Status**: ✅ FINAL

---

## Change Log

- **Sprint 0**: Initial decisions locked

---

**Note**: These decisions are final for v1.0. Any changes must be justified with a blocker or critical requirement change.


