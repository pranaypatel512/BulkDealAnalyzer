# Migration Rollback Guide

## Overview

Supabase migrations are **forward-only** by default. To rollback, you need to create a new migration that reverses the changes. This guide shows how to test rollback functionality.

## Understanding Rollback

**Important**: Supabase doesn't automatically track or reverse migrations. Rollback means:
1. Creating a **new migration** that undoes previous changes
2. Applying that migration to restore the previous state
3. Testing that the rollback works correctly

## Rollback Strategy

### When to Create Rollback Migrations

1. **Before Production Deployment**: Test rollback for critical migrations
2. **Emergency Situations**: Need to quickly revert a bad migration
3. **Development/Testing**: Validate rollback procedures

### Rollback Patterns

#### Pattern 1: Drop Tables (Initial Schema Rollback)

If you need to rollback the initial schema:

```sql
-- Rollback: Drop tables created in initial schema
DROP TABLE IF EXISTS bulk_deals CASCADE;
DROP TABLE IF EXISTS user_profiles CASCADE;

-- Drop functions
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;
```

#### Pattern 2: Recreate Deleted Tables (Cleanup Rollback)

If you need to restore tables deleted in cleanup:

```sql
-- Rollback: Recreate deleted tables (if you have structure)
CREATE TABLE IF NOT EXISTS submissions (
    -- original structure from backup
);
-- Recreate policies, indexes, etc.
```

## Testing Rollback

### Method 1: Manual Rollback Test

1. **Create Rollback Migration**:
   ```bash
   # Create new migration file
   touch supabase/migrations/YYYYMMDDHHMMSS_rollback_initial_schema.sql
   ```

2. **Write Rollback SQL**:
   ```sql
   -- Reverse changes from initial schema
   DROP TABLE IF EXISTS bulk_deals CASCADE;
   DROP TABLE IF EXISTS user_profiles CASCADE;
   DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;
   ```

3. **Test in Development**:
   ```bash
   # Apply rollback
   supabase db push
   
   # Verify tables are dropped
   supabase db execute "
   SELECT tablename FROM pg_tables 
   WHERE schemaname = 'public';
   "
   ```

4. **Re-apply Original Migration**:
   ```bash
   # The original migration should handle IF NOT EXISTS
   # So you can re-apply it
   ```

### Method 2: Using Test Script

Use the provided test script:
```bash
./scripts/test_migration_rollback.sh
```

## Rollback Test Script

The rollback test script will:
1. ✅ Verify current state
2. ✅ Apply rollback migration
3. ✅ Verify rollback succeeded
4. ✅ Optionally re-apply original migration
5. ✅ Verify final state

## Safe Rollback Practices

1. ✅ **Always Test in Development First**
2. ✅ **Create Backups Before Rollback**
3. ✅ **Use IF EXISTS** to prevent errors
4. ✅ **Use CASCADE** carefully (know what it affects)
5. ✅ **Document Rollback Steps**
6. ✅ **Test Re-application** after rollback

## Example: Rollback Initial Schema

```sql
-- File: supabase/migrations/20250101000002_rollback_initial_schema.sql
-- Rollback migration for initial schema

-- Step 1: Drop triggers first (depends on tables)
DROP TRIGGER IF EXISTS update_bulk_deals_updated_at ON bulk_deals CASCADE;
DROP TRIGGER IF EXISTS update_user_profiles_updated_at ON user_profiles CASCADE;

-- Step 2: Drop tables
DROP TABLE IF EXISTS bulk_deals CASCADE;
DROP TABLE IF EXISTS user_profiles CASCADE;

-- Step 3: Drop function
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- Verification
DO $$
BEGIN
    RAISE NOTICE 'Rollback completed: Initial schema removed';
END $$;
```

## Example: Re-apply After Rollback

After rollback, you can re-apply the original migration:

```bash
# Re-apply initial schema
supabase db push
```

The original migration uses `IF NOT EXISTS`, so it will recreate everything safely.

## Verification Steps

After rollback, verify:

1. **Tables Removed**:
   ```sql
   SELECT tablename 
   FROM pg_tables 
   WHERE schemaname = 'public' 
   AND tablename IN ('user_profiles', 'bulk_deals');
   ```
   Should return no rows.

2. **Functions Removed**:
   ```sql
   SELECT proname 
   FROM pg_proc 
   WHERE pronamespace = 'public'::regnamespace
   AND proname = 'update_updated_at_column';
   ```
   Should return no rows.

3. **Policies Removed**:
   ```sql
   SELECT policyname 
   FROM pg_policies 
   WHERE schemaname = 'public';
   ```
   Should return no rows (or only non-rolled-back policies).

## Production Rollback Considerations

⚠️ **Warning**: Production rollback requires:

1. **Data Backup**: Always backup before rollback
2. **Downtime Planning**: Rollback may require downtime
3. **Application Compatibility**: Ensure app works with rolled-back schema
4. **Testing**: Test rollback in staging first
5. **Documentation**: Document rollback steps and timing

## Quick Rollback Test

For a quick rollback test:

```bash
# 1. Verify current state
supabase migration list

# 2. Create rollback migration
# (create file with rollback SQL)

# 3. Apply rollback
supabase db push

# 4. Verify rollback
supabase db execute "
SELECT tablename FROM pg_tables 
WHERE schemaname = 'public';
"

# 5. Re-apply original (if needed)
# Migration files with IF NOT EXISTS can be re-applied
```

## Related Files

- `supabase/migrations/20250101000000_initial_schema.sql` - Initial schema
- `supabase/migrations/20250101000001_cleanup_database.sql` - Cleanup migration
- `scripts/test_migration_rollback.sh` - Rollback test script

