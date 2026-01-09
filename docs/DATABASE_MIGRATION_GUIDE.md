# Database Migration Guide

## Overview

This guide explains how to apply database migrations for the BulkDeal Analyzer platform.

## Prerequisites

1. **Supabase Project**: You need a Supabase project set up
2. **Database URL**: Connection string to your Supabase PostgreSQL database
3. **Supabase CLI** (optional but recommended): For easier migration management

## Migration Files

All migrations are stored in `supabase/migrations/`:

- `20250101000000_initial_schema.sql` - Initial schema with user_profiles and bulk_deals tables

## Method 1: Using Supabase CLI (Recommended)

### Install Supabase CLI

```bash
# macOS
brew install supabase/tap/supabase

# Linux
# Download from: https://github.com/supabase/cli/releases

# Windows
# Download from: https://github.com/supabase/cli/releases
```

### Setup

1. **Login to Supabase**:
   ```bash
   supabase login
   ```

2. **Link to your project**:
   ```bash
   supabase link --project-ref your-project-ref
   ```
   Find your project ref in Supabase dashboard URL or settings.

3. **Apply migrations**:
   ```bash
   supabase db push
   ```

### Verify

```bash
# Check migration status
supabase migration list

# Or verify via test script
python scripts/test_db_connection.py
```

## Method 2: Using Supabase Dashboard

1. **Open Supabase Dashboard**:
   - Go to: https://supabase.com/dashboard
   - Select your project

2. **Navigate to SQL Editor**:
   - Click "SQL Editor" in the left sidebar

3. **Apply Migration**:
   - Open `supabase/migrations/20250101000000_initial_schema.sql`
   - Copy entire file contents
   - Paste into SQL Editor
   - Click "Run" or press Cmd/Ctrl + Enter

4. **Verify**:
   - Go to "Table Editor"
   - Check that `user_profiles` and `bulk_deals` tables exist
   - Check "Authentication" → "Policies" to verify RLS policies

## Method 3: Using psql (Command Line)

```bash
# Set environment variable
export DATABASE_URL="postgresql://user:password@host:port/database"

# Apply migration
psql $DATABASE_URL -f supabase/migrations/20250101000000_initial_schema.sql
```

## Testing the Connection

After applying migrations, test the connection:

```bash
# Set DATABASE_URL in .env file or export it
export DATABASE_URL="postgresql://user:password@host:port/database"

# Run test script
python scripts/test_db_connection.py
```

The test script will verify:
- ✅ Tables exist
- ✅ RLS is enabled
- ✅ RLS policies are created
- ✅ Indexes are created
- ✅ Triggers are working

## Migration Structure

Migration files follow this naming convention:
- Format: `YYYYMMDDHHMMSS_description.sql`
- Example: `20250101000000_initial_schema.sql`

This ensures:
- Migrations run in chronological order
- Easy identification of when migration was created
- No naming conflicts

## Rollback Strategy

**IMPORTANT**: Always backup before running migrations in production.

### Manual Rollback

If you need to rollback a migration:

1. Create a new migration file with rollback SQL
2. Example: `20250101000001_rollback_initial_schema.sql`
3. Apply the rollback migration

### Backup Before Migration

```bash
# Using Supabase CLI
supabase db dump -f backup_before_migration.sql

# Or use pg_dump
pg_dump $DATABASE_URL > backup_before_migration.sql
```

## Verification Checklist

After applying migrations, verify:

- [ ] Tables `user_profiles` and `bulk_deals` exist in Table Editor
- [ ] RLS is enabled: Check table settings
- [ ] Policies exist: Authentication → Policies (8 policies total)
- [ ] Indexes exist: Run `\d bulk_deals` in SQL Editor
- [ ] Triggers work: Test by updating a record
- [ ] Connection test passes: `python scripts/test_db_connection.py`

## Troubleshooting

### Migration Fails

1. **Check error message** in Supabase SQL Editor
2. **Verify dependencies**: Ensure previous migrations were applied
3. **Check permissions**: Ensure database user has CREATE/ALTER permissions

### RLS Not Working

1. **Verify RLS is enabled**:
   ```sql
   SELECT tablename, rowsecurity FROM pg_tables 
   WHERE tablename IN ('user_profiles', 'bulk_deals');
   ```

2. **Check policies exist**:
   ```sql
   SELECT * FROM pg_policies 
   WHERE tablename IN ('user_profiles', 'bulk_deals');
   ```

### Connection Issues

1. **Verify DATABASE_URL format**:
   ```
   postgresql://user:password@host:port/database
   ```

2. **Check firewall/network**: Supabase allows connections from anywhere by default

3. **Verify credentials**: Check Supabase project settings

## Next Steps

After successful migration:

1. ✅ Update `.env` file with `DATABASE_URL`
2. ✅ Run connection test: `python scripts/test_db_connection.py`
3. ✅ Start backend development with database integration
4. ✅ Move GitHub Project card to "In Progress"

## Related Files

- `supabase/migrations/20250101000000_initial_schema.sql` - Migration file
- `docs/database_schema_draft.md` - Complete schema documentation
- `scripts/test_db_connection.py` - Connection test script

