# Supabase Migrations

This directory contains Supabase database migrations for the BulkDeal Analyzer platform.

## Migration Files

- `20250101000000_initial_schema.sql` - Initial schema with user_profiles and bulk_deals tables

## Applying Migrations

### Using Supabase CLI (Recommended)

```bash
# Install Supabase CLI if not installed
# https://supabase.com/docs/guides/cli

# Login to Supabase
supabase login

# Link to your project
supabase link --project-ref your-project-ref

# Apply migrations
supabase db push
```

### Using Supabase Dashboard

1. Go to your Supabase project dashboard
2. Navigate to: SQL Editor
3. Copy and paste migration SQL
4. Run the migration

### Manual Application

1. Open Supabase SQL Editor
2. Copy contents of migration file
3. Paste and execute
4. Verify tables were created: Check "Table Editor" tab

## Migration Guidelines

1. **Always backup** before running migrations in production
2. **Test migrations** in development/staging first
3. **Never modify** existing migration files after they've been applied
4. **Use descriptive names** with timestamp prefix: `YYYYMMDDHHMMSS_description.sql`
5. **Include rollback** instructions in migration comments if needed

## Rollback

To rollback a migration, create a new migration file that reverses the changes.

Example:
- Migration: `20250101000000_create_table.sql`
- Rollback: `20250101000001_drop_table.sql`

## Verification

After applying migrations, verify:

1. Tables exist: Check in Supabase Table Editor
2. RLS is enabled: `SELECT * FROM pg_policies WHERE tablename = 'bulk_deals';`
3. Indexes exist: `SELECT indexname FROM pg_indexes WHERE tablename = 'bulk_deals';`
4. Triggers exist: `SELECT * FROM pg_trigger WHERE tgname LIKE '%updated_at%';`

