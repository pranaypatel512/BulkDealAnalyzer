# Database Cleanup Guide

## Overview

This guide helps you clean up your Supabase database to remove all existing tables, policies, and other objects except those created by our migration script.

## What Gets Preserved

The cleanup script preserves only:

### Tables
- ✅ `user_profiles`
- ✅ `bulk_deals`

### Policies
- ✅ "Users can view own profile"
- ✅ "Users can insert own profile"
- ✅ "Users can update own profile"
- ✅ "Users can delete own profile"
- ✅ "Users can view own deals"
- ✅ "Users can insert own deals"
- ✅ "Users can update own deals"
- ✅ "Users can delete own deals"

### Functions & Triggers
- ✅ `update_updated_at_column()` function
- ✅ Triggers on `user_profiles` and `bulk_deals`

## What Gets Deleted

- ❌ All other tables in `public` schema
- ❌ All other policies
- ❌ All other functions
- ❌ All other triggers
- ❌ All views
- ❌ All custom types

**Note**: The `auth` schema and system tables are NOT affected.

## ⚠️ WARNING

**This action is IRREVERSIBLE!** Make sure you:
1. ✅ Have a backup if you need to restore anything
2. ✅ Have verified the migration is working
3. ✅ Understand what will be deleted

## Usage

### Option 1: Using the Script (Recommended)

```bash
./scripts/cleanup_database.sh
```

The script will:
1. ✅ Check prerequisites (Supabase CLI, project link)
2. ✅ Show preview of what will be deleted
3. ✅ Ask for confirmation (twice)
4. ✅ Execute cleanup
5. ✅ Verify remaining objects

### Option 2: Manual SQL Execution

1. **Preview what will be deleted**:
   ```bash
   supabase db execute "
   SELECT tablename 
   FROM pg_tables 
   WHERE schemaname = 'public' 
   AND tablename NOT IN ('user_profiles', 'bulk_deals');
   "
   ```

2. **Create backup** (optional but recommended):
   ```bash
   supabase db dump -f backup_before_cleanup.sql
   ```

3. **Run cleanup**:
   ```bash
   supabase db execute < scripts/cleanup_database.sh
   ```

### Option 3: Using Supabase Dashboard

1. Go to: Supabase Dashboard → SQL Editor
2. Copy the SQL from `scripts/cleanup_database.sh` (between the SQL markers)
3. Review carefully
4. Execute

## Before Running Cleanup

1. ✅ **Verify migration is applied**:
   ```bash
   supabase migration list
   ```

2. ✅ **Verify our tables exist**:
   ```bash
   supabase db execute "
   SELECT tablename 
   FROM pg_tables 
   WHERE schemaname = 'public' 
   AND tablename IN ('user_profiles', 'bulk_deals');
   "
   ```

3. ✅ **Create backup** (if needed):
   ```bash
   supabase db dump -f backup_$(date +%Y%m%d_%H%M%S).sql
   ```

## After Cleanup

1. ✅ **Verify tables**:
   ```bash
   supabase db execute "
   SELECT tablename 
   FROM pg_tables 
   WHERE schemaname = 'public';
   "
   ```
   Should only show: `user_profiles`, `bulk_deals`

2. ✅ **Verify policies**:
   ```bash
   supabase db execute "
   SELECT tablename, policyname 
   FROM pg_policies 
   WHERE schemaname = 'public';
   "
   ```
   Should show 8 policies (4 for each table)

3. ✅ **Run connection test**:
   ```bash
   python3 scripts/test_db_connection.py
   ```

4. ✅ **Check in Supabase Dashboard**:
   - Table Editor: Should only show 2 tables
   - Authentication → Policies: Should show 8 policies

## Troubleshooting

### Cleanup Fails

If cleanup fails:
1. Check error message in the script output
2. Common issues:
   - Foreign key constraints: Some tables might reference others
   - Permission issues: Check database user permissions
   - Connection issues: Verify Supabase CLI is linked

### Accidentally Deleted Important Tables

If you need to restore:
1. Use your backup (if created):
   ```bash
   supabase db execute < backup_before_cleanup.sql
   ```
2. Or restore from Supabase dashboard backups (if enabled)

### Verification Shows Unexpected Tables

If you see tables other than `user_profiles` and `bulk_deals`:
1. Check if they're system tables (usually in `information_schema` or `pg_catalog`)
2. If in `public` schema, they might be from migrations that ran after cleanup
3. Re-run cleanup if needed

## Safety Features

The cleanup script includes:
- ✅ Double confirmation (requires typing "yes" twice)
- ✅ Preview of what will be deleted
- ✅ Preserves only our migration objects
- ✅ Does not affect `auth` schema
- ✅ Does not affect system schemas

## Related Files

- `scripts/cleanup_database.sh` - Cleanup script
- `supabase/migrations/20250101000000_initial_schema.sql` - Our migration
- `scripts/test_db_connection.py` - Verification script

