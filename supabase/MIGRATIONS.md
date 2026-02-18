# Supabase Migrations

Migrations live in `supabase/migrations/`. Only files matching `<timestamp>_name.sql` are run by `supabase db push`.

## Migration Files

- `20250101000000_initial_schema.sql` - Initial schema (user_profiles, bulk_deals, etc.)
- `20250101000001_cleanup_database.sql` - Cleanup
- `20250216000000_fetch_history.sql` - Fetch history table
- `20250216000001_watchlist.sql` - Watchlist & alerts tables
- `20250216000002_user_role.sql` - User role
- `20250216100000_block_deals_short_selling.sql` - Block deals & short selling tables

## Applying Migrations

### Using Supabase CLI (Recommended)

```bash
supabase login
supabase link --project-ref YOUR_PROJECT_REF
supabase db push
```

### Using Supabase Dashboard

1. Go to your Supabase project dashboard → **SQL Editor**
2. Copy contents of the migration file
3. Paste and run

## Guidelines

1. **Backup** before running migrations in production
2. **Test** in development/staging first
3. **Do not modify** existing migration files after they have been applied
4. Use **descriptive names** with timestamp prefix: `YYYYMMDDHHMMSS_description.sql`
5. Use **DROP POLICY IF EXISTS** / **DROP TRIGGER IF EXISTS** before CREATE when making migrations idempotent (safe to re-run)

## Verification

After applying: check Table Editor, RLS policies, and indexes in the Supabase dashboard.
