## API Versioning & Migration Strategy

### Overview

API versioning ensures backward compatibility and allows gradual migration of clients to new API versions. This section outlines the versioning strategy and migration process.

### API Versioning Strategy

#### Versioning Approach: URL Path Versioning

**Format**: `/api/v{version}/{endpoint}`

**Examples**:
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

```
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

**Tool**: Supabase CLI with SQL migration files

**Location**: `supabase/migrations/`

**Format**: `{timestamp}_{description}.sql`

**Example**: `20240115120000_create_user_profiles.sql`

### Migration File Structure

```
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

**Format**: `{YYYYMMDDHHMMSS}_{description}.sql`

**Examples**:
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

```
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

**Location**: Root of repository

**Content**:

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
```
type(module): Short description

Longer description if needed

- Bullet point 1
- Bullet point 2
```

**Types**: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

**Examples**:
```
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


